from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")

    # Ensure auth & authorization tables exist (safe - does not modify existing data)
    try:
        from app.core.database.session import engine
        from app.core.auth.models import UserSession
        from app.core.authorization.models import Permission, RolePermission, UserRole
        from app.models.activity_log import ActivityLog
        from app.models.audit_log import AuditLog
        UserSession.__table__.create(bind=engine, checkfirst=True)
        Permission.__table__.create(bind=engine, checkfirst=True)
        RolePermission.__table__.create(bind=engine, checkfirst=True)
        UserRole.__table__.create(bind=engine, checkfirst=True)
        ActivityLog.__table__.create(bind=engine, checkfirst=True)
        AuditLog.__table__.create(bind=engine, checkfirst=True)
    except Exception as e:
        logger.warning("Auth table creation skipped: %s", e)

    # Add missing columns to users table (safe for old schemas)
    try:
        with engine.connect() as conn:
            from sqlalchemy import inspect, text as sql_text
            inspector = inspect(engine)
            existing_cols = {c["name"] for c in inspector.get_columns("users")}
            missing_user_cols = {
                "is_verified": "BOOLEAN DEFAULT FALSE",
                "must_change_password": "BOOLEAN DEFAULT FALSE",
                "password_changed_at": "DATETIME NULL",
                "last_login": "DATETIME NULL",
                "created_at": "DATETIME NULL",
                "updated_at": "DATETIME NULL",
            }
            for col_name, col_def in missing_user_cols.items():
                if col_name not in existing_cols:
                    conn.execute(sql_text(
                        f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"
                    ))
                    logger.info("Added missing column users.%s", col_name)

            # Add is_system column to roles table
            if "roles" in inspector.get_table_names():
                role_cols = {c["name"] for c in inspector.get_columns("roles")}
                if "is_system" not in role_cols:
                    conn.execute(sql_text(
                        "ALTER TABLE roles ADD COLUMN is_system BOOLEAN DEFAULT TRUE"
                    ))
                    logger.info("Added missing column roles.is_system")

            conn.commit()
    except Exception as e:
        logger.warning("Schema migration skipped: %s", e)

    from app.core.cache import cache_service
    await cache_service.initialize()

    from app.core.notification import notification_service
    from app.core.notification.channels.in_app import InAppChannel
    from app.core.notification.channels.email import EmailChannel
    notification_service.register_channel(InAppChannel())
    notification_service.register_channel(EmailChannel())

    try:
        from app.core.database.session import SessionLocal
        from app.core.authorization.services import sync_permissions_from_enum, sync_role_permissions_from_enum
        db = SessionLocal()
        try:
            sync_permissions_from_enum(db)
            sync_role_permissions_from_enum(db)
        except Exception as e:
            logger.warning("Permission sync failed (DB may not be migrated yet): %s", e)
        finally:
            db.close()
    except Exception as e:
        logger.warning("Startup sync skipped: %s", e)

    yield

    await cache_service.close()
    logger.info("Application shutting down...")
