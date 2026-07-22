from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from pydantic import BaseModel
from app.core.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 10, 
        search: Optional[str] = None, 
        search_fields: List[str] = None,
        sort_by: Optional[str] = "id", 
        sort_order: Optional[str] = "desc",
        filters: Dict[str, Any] = None
    ) -> tuple[List[ModelType], int]:
        """
        Returns a tuple of (list of records, total count).
        Supports pagination, generic filtering, search on specific fields, and sorting.
        """
        query = db.query(self.model)

        # Apply exact match filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)

        # Apply search on specified fields (ILIKE for case-insensitive)
        if search and search_fields:
            search_conditions = []
            for field in search_fields:
                if hasattr(self.model, field):
                    search_conditions.append(getattr(self.model, field).ilike(f"%{search}%"))
            if search_conditions:
                query = query.filter(or_(*search_conditions))

        # Total count before pagination
        total = query.count()

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            order_func = desc if sort_order == "desc" else asc
            query = query.order_by(order_func(getattr(self.model, sort_by)))
        
        # Apply pagination
        if limit > 0:
            query = query.offset(skip).limit(limit)
            
        return query.all(), total

    def create(self, db: Session, obj_in: CreateSchemaType | Dict[str, Any], commit: bool = True) -> ModelType:
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        else:
            db.flush()
        return db_obj

    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
        commit: bool = True
    ) -> ModelType:
        obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
        
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        else:
            db.flush()
        return db_obj

    def delete(self, db: Session, id: Any) -> Optional[ModelType]:
        obj = self.get_by_id(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
