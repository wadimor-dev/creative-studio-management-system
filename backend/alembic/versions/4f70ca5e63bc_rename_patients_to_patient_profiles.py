"""rename_patients_to_patient_profiles (idempotent)

Handles partial application from a previous failed run.
Checks current DB state and only applies missing changes.
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '4f70ca5e63bc'
down_revision: Union[str, Sequence[str], None] = '001a0b0c0d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


def _fk_exists(table: str, fk_name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS "
        "WHERE CONSTRAINT_SCHEMA = DATABASE() AND TABLE_NAME = :t "
        "AND CONSTRAINT_NAME = :f AND CONSTRAINT_TYPE = 'FOREIGN KEY'"
    ), {"t": table, "f": fk_name})
    return r.scalar() > 0


def _index_exists(table: str, idx_name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.STATISTICS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t "
        "AND INDEX_NAME = :i"
    ), {"t": table, "i": idx_name})
    return r.scalar() > 0


def _column_exists(table: str, col: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t "
        "AND COLUMN_NAME = :c"
    ), {"t": table, "c": col})
    return r.scalar() > 0


def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Drop FK visits.patient_id / patient_profile_id → patients.id ──
    if _table_exists('visits') and _fk_exists('visits', 'visits_ibfk_1'):
        with op.batch_alter_table('visits') as batch_op:
            batch_op.drop_constraint('visits_ibfk_1', type_='foreignkey')

    # ── 2. Drop FKs on patients.created_by / updated_by → users.id ──
    if _table_exists('patients'):
        with op.batch_alter_table('patients') as batch_op:
            if _fk_exists('patients', 'patients_ibfk_2'):
                batch_op.drop_constraint('patients_ibfk_2', type_='foreignkey')
            if _fk_exists('patients', 'patients_ibfk_3'):
                batch_op.drop_constraint('patients_ibfk_3', type_='foreignkey')

    # ── 3. Rename visits.patient_id → visits.patient_profile_id ──
    if _table_exists('visits') and _column_exists('visits', 'patient_id') and not _column_exists('visits', 'patient_profile_id'):
        op.alter_column('visits', 'patient_id', new_column_name='patient_profile_id',
                        existing_type=sa.String(36), nullable=False)

    # ── 4. Convert rhesus values: '+' → 'POSITIVE', '-' → 'NEGATIVE' ──
    if _table_exists('patients'):
        conn.execute(sa.text("UPDATE patients SET rhesus = 'POSITIVE' WHERE rhesus = '+'"))
        conn.execute(sa.text("UPDATE patients SET rhesus = 'NEGATIVE' WHERE rhesus = '-'"))

    # ── 5. Alter rhesus_enum type ──
    if _table_exists('patients') and _column_exists('patients', 'rhesus'):
        # Check if we need to alter by verifying if '+' is a valid enum value
        try:
            conn.execute(sa.text("INSERT INTO patients (id, employee_id, medical_record_number, rhesus, created_at, updated_at) "
                                "VALUES ('_test_rhesus_', 0, '_test_rhesus_', '+', NOW(), NOW())"))
            conn.execute(sa.text("DELETE FROM patients WHERE id = '_test_rhesus_'"))
            # '+' is accepted, so we need to alter
            op.alter_column('patients', 'rhesus',
                            existing_type=mysql.ENUM('+', '-'),
                            type_=mysql.ENUM('POSITIVE', 'NEGATIVE'),
                            nullable=True)
        except Exception:
            pass  # Already altered or doesn't need altering

    # ── 6. Rename patients → patient_profiles ──
    if _table_exists('patients') and not _table_exists('patient_profiles'):
        op.rename_table('patients', 'patient_profiles')

    # ── 7. Recreate missing FKs ──
    if _table_exists('patient_profiles'):
        if not _fk_exists('patient_profiles', 'patient_profiles_ibfk_1'):
            op.create_foreign_key('patient_profiles_ibfk_1', 'patient_profiles', 'employees',
                                  ['employee_id'], ['id'], ondelete='RESTRICT')
        if not _fk_exists('patient_profiles', 'patient_profiles_ibfk_2'):
            op.create_foreign_key('patient_profiles_ibfk_2', 'patient_profiles', 'users',
                                  ['created_by'], ['id'])
        if not _fk_exists('patient_profiles', 'patient_profiles_ibfk_3'):
            op.create_foreign_key('patient_profiles_ibfk_3', 'patient_profiles', 'users',
                                  ['updated_by'], ['id'])

    if _table_exists('visits') and not _fk_exists('visits', 'visits_ibfk_1'):
        op.create_foreign_key('visits_ibfk_1', 'visits', 'patient_profiles',
                              ['patient_profile_id'], ['id'], ondelete='RESTRICT')

    # ── 8. Clean up test row if it exists ──
    conn.execute(sa.text("DELETE FROM patient_profiles WHERE id = '_test_rhesus_'"))


def downgrade() -> None:
    conn = op.get_bind()

    # ── Drop FKs if they exist ──
    if _table_exists('patient_profiles'):
        with op.batch_alter_table('patient_profiles') as batch_op:
            for fk in ['patient_profiles_ibfk_1', 'patient_profiles_ibfk_2', 'patient_profiles_ibfk_3']:
                if _fk_exists('patient_profiles', fk):
                    batch_op.drop_constraint(fk, type_='foreignkey')

    if _table_exists('visits') and _fk_exists('visits', 'visits_ibfk_1'):
        with op.batch_alter_table('visits') as batch_op:
            batch_op.drop_constraint('visits_ibfk_1', type_='foreignkey')

    # ── Rename back ──
    if _table_exists('patient_profiles') and not _table_exists('patients'):
        op.rename_table('patient_profiles', 'patients')

    # ── Restore rhesus_enum ──
    if _table_exists('patients') and _column_exists('patients', 'rhesus'):
        conn.execute(sa.text("UPDATE patients SET rhesus = '+' WHERE rhesus = 'POSITIVE'"))
        conn.execute(sa.text("UPDATE patients SET rhesus = '-' WHERE rhesus = 'NEGATIVE'"))
        try:
            conn.execute(sa.text("SELECT CAST('POSITIVE' AS CHAR(10))"))
        except Exception:
            pass
        op.alter_column('patients', 'rhesus',
                        existing_type=mysql.ENUM('POSITIVE', 'NEGATIVE'),
                        type_=mysql.ENUM('+', '-'),
                        nullable=True)

    # ── Rename column back ──
    if _table_exists('visits') and _column_exists('visits', 'patient_profile_id') and not _column_exists('visits', 'patient_id'):
        op.alter_column('visits', 'patient_profile_id', new_column_name='patient_id',
                        existing_type=sa.String(36), nullable=False)

    # ── Recreate FKs on patients ──
    if _table_exists('patients'):
        if not _fk_exists('patients', 'patients_ibfk_2'):
            op.create_foreign_key('patients_ibfk_2', 'patients', 'users', ['created_by'], ['id'])
        if not _fk_exists('patients', 'patients_ibfk_3'):
            op.create_foreign_key('patients_ibfk_3', 'patients', 'users', ['updated_by'], ['id'])
    if _table_exists('visits') and _table_exists('patients') and not _fk_exists('visits', 'visits_ibfk_1'):
        op.create_foreign_key('visits_ibfk_1', 'visits', 'patients',
                              ['patient_id'], ['id'], ondelete='RESTRICT')
