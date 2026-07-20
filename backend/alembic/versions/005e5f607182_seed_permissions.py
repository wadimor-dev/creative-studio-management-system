"""005 backfill permissions seed data

Revision ID: 005e5f607182
Revises: 004d4e5f6071
Create Date: 2026-07-19 12:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '005e5f607182'
down_revision: Union[str, Sequence[str], None] = '004d4e5f6071'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PERMISSIONS = [
    ("SHOWROOM_VIEW", "View Showroom", "View showroom data and reports"),
    ("SHOWROOM_CREATE", "Create Showroom", "Create stock entries and movements"),
    ("SHOWROOM_MOVE", "Move Stock", "Transfer stock between locations"),
    ("SHOWROOM_BORROW", "Borrow Stock", "Borrow stock for external use"),
    ("SHOWROOM_RELEASE", "Release to Guest", "Release stock to guests"),
    ("SHOWROOM_MAINTENANCE", "Maintenance", "Manage maintenance requests"),
    ("SHOWROOM_OPNAME", "Opname", "Perform stock opname"),
    ("SHOWROOM_ADJUST", "Adjust Stock", "Adjust stock quantities"),
    ("SHOWROOM_MANAGE", "Manage Showroom", "Manage locations and master data"),
    ("SHOWROOM_APPROVE", "Approve Operations", "Approve requests and opname"),
    ("SHOWROOM_REPORT", "View Reports", "Access reporting and analytics"),
    ("SHOWROOM_ADMIN", "Admin Showroom", "Full admin access to showroom"),
]

ROLES = [
    ("VIEWER", "Viewer", "View-only access to showroom data", 1),
    ("OPERATOR", "Operator", "Can perform stock operations", 1),
    ("SUPERVISOR", "Supervisor", "Can approve and manage operations", 1),
    ("ADMIN", "Admin", "Full admin access to showroom", 1),
]

ROLE_PERMISSIONS = {
    "VIEWER": ["SHOWROOM_VIEW", "SHOWROOM_REPORT"],
    "OPERATOR": ["SHOWROOM_VIEW", "SHOWROOM_CREATE", "SHOWROOM_MOVE", "SHOWROOM_BORROW", "SHOWROOM_RELEASE", "SHOWROOM_MAINTENANCE", "SHOWROOM_ADJUST"],
    "SUPERVISOR": ["SHOWROOM_VIEW", "SHOWROOM_CREATE", "SHOWROOM_MOVE", "SHOWROOM_BORROW", "SHOWROOM_RELEASE", "SHOWROOM_MAINTENANCE", "SHOWROOM_OPNAME", "SHOWROOM_ADJUST", "SHOWROOM_MANAGE", "SHOWROOM_APPROVE", "SHOWROOM_REPORT"],
    "ADMIN": [p[0] for p in PERMISSIONS],
}


def upgrade() -> None:
    conn = op.get_bind()

    existing_perms = conn.execute(sa.text("SELECT code FROM showroom_permissions")).fetchall()
    existing_codes = {r[0] for r in existing_perms}

    for code, name, desc in PERMISSIONS:
        if code not in existing_codes:
            conn.execute(sa.text(
                "INSERT INTO showroom_permissions (code, name, description, created_at) "
                "VALUES (:code, :name, :desc, NOW())"
            ), {"code": code, "name": name, "desc": desc})

    existing_roles = conn.execute(sa.text("SELECT code FROM showroom_roles")).fetchall()
    existing_role_codes = {r[0] for r in existing_roles}

    for code, name, desc, is_system in ROLES:
        if code not in existing_role_codes:
            conn.execute(sa.text(
                "INSERT INTO showroom_roles (code, name, description, is_system, created_at, updated_at) "
                "VALUES (:code, :name, :desc, :is_sys, NOW(), NOW())"
            ), {"code": code, "name": name, "desc": desc, "is_sys": is_system})

    all_perms = conn.execute(sa.text("SELECT id, code FROM showroom_permissions")).fetchall()
    perm_id_map = {r[1]: r[0] for r in all_perms}

    all_roles = conn.execute(sa.text("SELECT id, code FROM showroom_roles")).fetchall()
    role_id_map = {r[1]: r[0] for r in all_roles}

    existing_rp = conn.execute(sa.text("SELECT role_id, permission_id FROM showroom_role_permissions")).fetchall()
    existing_rp_set = {(r[0], r[1]) for r in existing_rp}

    for role_code, perm_codes in ROLE_PERMISSIONS.items():
        role_id = role_id_map.get(role_code)
        if not role_id:
            continue
        for perm_code in perm_codes:
            perm_id = perm_id_map.get(perm_code)
            if perm_id and (role_id, perm_id) not in existing_rp_set:
                conn.execute(sa.text(
                    "INSERT INTO showroom_role_permissions (role_id, permission_id, created_at) "
                    "VALUES (:rid, :pid, NOW())"
                ), {"rid": role_id, "pid": perm_id})


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM showroom_role_permissions WHERE role_id IN (SELECT id FROM showroom_roles WHERE is_system = 1)"))
    conn.execute(sa.text("DELETE FROM showroom_user_roles WHERE role_id IN (SELECT id FROM showroom_roles WHERE is_system = 1)"))
    conn.execute(sa.text("DELETE FROM showroom_roles WHERE is_system = 1"))
    conn.execute(sa.text("DELETE FROM showroom_permissions WHERE code IN ('SHOWROOM_VIEW','SHOWROOM_CREATE','SHOWROOM_MOVE','SHOWROOM_BORROW','SHOWROOM_RELEASE','SHOWROOM_MAINTENANCE','SHOWROOM_OPNAME','SHOWROOM_ADJUST','SHOWROOM_MANAGE','SHOWROOM_APPROVE','SHOWROOM_REPORT','SHOWROOM_ADMIN')"))
