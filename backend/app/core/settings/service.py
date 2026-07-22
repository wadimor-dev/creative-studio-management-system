from typing import Optional, List, Any
from sqlalchemy.orm import Session
import json
from app.core.settings.models import SystemSetting
from app.core.settings.schemas import SystemSettingCreate, SystemSettingUpdate
from app.core.database.helpers import get_or_404
from app.core.exceptions import CSMSException


class SettingsService:

    def get_all(self, db: Session) -> List[SystemSetting]:
        return db.query(SystemSetting).order_by(SystemSetting.key).all()

    def get_public(self, db: Session) -> List[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.is_public == True).all()

    def get_by_key(self, db: Session, key: str) -> Optional[SystemSetting]:
        return db.query(SystemSetting).filter(SystemSetting.key == key).first()

    def get_value(self, db: Session, key: str, default: Any = None) -> Any:
        setting = self.get_by_key(db, key)
        if not setting or not setting.value:
            return default
        try:
            return json.loads(setting.value)
        except (json.JSONDecodeError, TypeError):
            return setting.value

    def set(self, db: Session, key: str, value: Any, description: Optional[str] = None,
            is_public: bool = False) -> SystemSetting:
        setting = self.get_by_key(db, key)
        string_value = json.dumps(value) if not isinstance(value, str) else value
        if setting:
            setting.value = string_value
            if description is not None:
                setting.description = description
            setting.is_public = is_public
        else:
            setting = SystemSetting(
                key=key, value=string_value,
                description=description, is_public=is_public,
            )
            db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting

    def create(self, db: Session, data: SystemSettingCreate) -> SystemSetting:
        existing = self.get_by_key(db, data.key)
        if existing:
            raise CSMSException(f"Setting '{data.key}' already exists", status_code=409)
        setting = SystemSetting(**data.model_dump())
        db.add(setting)
        db.commit()
        db.refresh(setting)
        return setting

    def update(self, db: Session, setting_id: int, data: SystemSettingUpdate) -> SystemSetting:
        setting = get_or_404(db, SystemSetting, setting_id, "Setting")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(setting, field, value)
        db.commit()
        db.refresh(setting)
        return setting

    def delete(self, db: Session, key: str) -> None:
        setting = self.get_by_key(db, key)
        if setting:
            db.delete(setting)
            db.commit()


settings_service = SettingsService()
