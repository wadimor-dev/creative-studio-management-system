from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from app.database.base import Base


showroom_role_permissions = Table(
    "showroom_role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("showroom_roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("showroom_permissions.id"), primary_key=True),
    Column("created_at", DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None)),
)


class ShowroomPermission(Base):
    __tablename__ = "showroom_permissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    roles = relationship("ShowroomRole", secondary=showroom_role_permissions, back_populates="permissions")


class ShowroomRole(Base):
    __tablename__ = "showroom_roles"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    is_system = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    permissions = relationship("ShowroomPermission", secondary=showroom_role_permissions, back_populates="roles")
    user_roles = relationship("ShowroomUserRole", back_populates="role")


class ShowroomUserRole(Base):
    __tablename__ = "showroom_user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(Integer, ForeignKey("showroom_roles.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    role = relationship("ShowroomRole", back_populates="user_roles")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
