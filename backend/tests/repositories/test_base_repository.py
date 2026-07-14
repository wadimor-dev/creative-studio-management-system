import pytest
from app.repositories.base_repository import BaseRepository
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class TestCategoryRepository:
    def test_create(self, db):
        repo = BaseRepository[Category, CategoryCreate, CategoryUpdate](Category)
        obj_in = CategoryCreate(name="Test Category", description="Desc")
        
        category = repo.create(db, obj_in=obj_in)
        assert category.id is not None
        assert category.name == "Test Category"
        assert category.description == "Desc"

    def test_get_by_id(self, db):
        repo = BaseRepository[Category, CategoryCreate, CategoryUpdate](Category)
        category = repo.create(db, obj_in={"name": "Get Me"})
        
        fetched = repo.get_by_id(db, category.id)
        assert fetched is not None
        assert fetched.name == "Get Me"

    def test_update(self, db):
        repo = BaseRepository[Category, CategoryCreate, CategoryUpdate](Category)
        category = repo.create(db, obj_in={"name": "Old Name"})
        
        updated = repo.update(db, db_obj=category, obj_in={"name": "New Name"})
        assert updated.name == "New Name"

    def test_delete(self, db):
        repo = BaseRepository[Category, CategoryCreate, CategoryUpdate](Category)
        category = repo.create(db, obj_in={"name": "Delete Me"})
        
        deleted = repo.delete(db, category.id)
        assert deleted is not None
        assert deleted.name == "Delete Me"
        
        fetched = repo.get_by_id(db, category.id)
        assert fetched is None

    def test_get_all(self, db):
        repo = BaseRepository[Category, CategoryCreate, CategoryUpdate](Category)
        repo.create(db, obj_in={"name": "Cat 1"})
        repo.create(db, obj_in={"name": "Cat 2"})
        
        cats, total = repo.get_all(db)
        assert total == 2
        assert len(cats) == 2
