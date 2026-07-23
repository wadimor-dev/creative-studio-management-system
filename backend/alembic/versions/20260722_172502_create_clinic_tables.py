"""create_clinic_tables — all 17 clinic module tables

Revision ID: 001a0b0c0d0e
Revises: 4f2500b21ba9
Create Date: 2026-07-22 07:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '001a0b0c0d0e'
down_revision: Union[str, Sequence[str], None] = '4f2500b21ba9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(name: str) -> bool:
    conn = op.get_bind()
    r = conn.execute(sa.text(
        "SELECT COUNT(*) FROM information_schema.tables "
        "WHERE table_schema = DATABASE() AND table_name = :t"
    ), {"t": name})
    return r.scalar() > 0


def upgrade() -> None:
    # ── 1. PATIENT PROFILES ──
    if not _table_exists('patient_profiles'):
        op.create_table('patient_profiles',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id', ondelete='RESTRICT'), nullable=False, unique=True),
            sa.Column('medical_record_number', sa.String(30), nullable=False, unique=True),
            sa.Column('blood_type', sa.Enum('A', 'B', 'AB', 'O', name='blood_type_enum'), nullable=True),
            sa.Column('rhesus', sa.Enum('+', '-', name='rhesus_enum'), nullable=True),
            sa.Column('allergy_note', sa.Text(), nullable=True),
            sa.Column('emergency_contact_name', sa.String(100), nullable=True),
            sa.Column('emergency_contact_phone', sa.String(30), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('updated_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_patient_profiles_id', 'patient_profiles', ['id'])
        op.create_index('ix_patient_profiles_employee_id', 'patient_profiles', ['employee_id'], unique=True)
        op.create_index('ix_patient_profiles_medical_record_number', 'patient_profiles', ['medical_record_number'], unique=True)

    # ── 2. HEALTHCARE PROFESSIONALS ──
    if not _table_exists('healthcare_professionals'):
        op.create_table('healthcare_professionals',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('employee_id', sa.Integer(), sa.ForeignKey('employees.id', ondelete='RESTRICT'), nullable=False, unique=True),
            sa.Column('profession', sa.Enum('DOCTOR', 'NURSE', 'MIDWIFE', 'LAB_TECHNICIAN', 'PHARMACIST', 'DENTIST', 'OTHER', name='profession_enum'), nullable=False),
            sa.Column('specialization', sa.String(100), nullable=True),
            sa.Column('license_number', sa.String(50), nullable=True),
            sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'SUSPENDED', name='prof_status_enum'), nullable=False, server_default=sa.text("'ACTIVE'")),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_hp_id', 'healthcare_professionals', ['id'])
        op.create_index('ix_hp_employee_id', 'healthcare_professionals', ['employee_id'], unique=True)
        op.create_index('ix_hp_license_number', 'healthcare_professionals', ['license_number'])

    # ── 3. ICD-10 CODES ──
    if not _table_exists('icd10_codes'):
        op.create_table('icd10_codes',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('code', sa.String(20), nullable=False, unique=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('is_active', sa.Integer(), nullable=False, server_default=sa.text('1')),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_icd10_id', 'icd10_codes', ['id'])
        op.create_index('ix_icd10_code', 'icd10_codes', ['code'], unique=True)

    # ── 4. MEDICAL PROCEDURES ──
    if not _table_exists('medical_procedures'):
        op.create_table('medical_procedures',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('code', sa.String(50), nullable=False, unique=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_mp_id', 'medical_procedures', ['id'])
        op.create_index('ix_mp_code', 'medical_procedures', ['code'], unique=True)

    # ── 5. QUEUES ──
    if not _table_exists('queues'):
        op.create_table('queues',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('queue_number', sa.String(20), nullable=False),
            sa.Column('queue_date', sa.Date(), nullable=False),
            sa.Column('status', sa.Enum('WAITING', 'CALLING', 'SERVING', 'FINISHED', 'CANCELLED', name='queue_status_enum'), nullable=False, server_default=sa.text("'WAITING'")),
            sa.Column('called_at', sa.DateTime(), nullable=True),
            sa.Column('finished_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_queues_id', 'queues', ['id'])
        op.create_index('ix_queues_date', 'queues', ['queue_date'])

    # ── 6. VISITS ──
    if not _table_exists('visits'):
        op.create_table('visits',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_number', sa.String(30), nullable=False, unique=True),
            sa.Column('patient_profile_id', sa.String(36), sa.ForeignKey('patient_profiles.id', ondelete='RESTRICT'), nullable=False),
            sa.Column('queue_id', sa.String(36), sa.ForeignKey('queues.id', ondelete='SET NULL'), nullable=True, unique=True),
            sa.Column('healthcare_professional_id', sa.String(36), sa.ForeignKey('healthcare_professionals.id', ondelete='SET NULL'), nullable=True),
            sa.Column('visit_type', sa.Enum('REGULAR', 'EMERGENCY', 'FOLLOW_UP', name='visit_type_enum'), nullable=False, server_default=sa.text("'REGULAR'")),
            sa.Column('visit_date', sa.DateTime(), nullable=False),
            sa.Column('complaint', sa.Text(), nullable=True),
            sa.Column('visit_status', sa.Enum('CHECKIN', 'SERVING', 'FINISHED', 'CANCELLED', name='visit_status_enum'), nullable=False, server_default=sa.text("'CHECKIN'")),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_visits_id', 'visits', ['id'])
        op.create_index('ix_visits_number', 'visits', ['visit_number'], unique=True)
        op.create_index('ix_visits_patient_profile_id', 'visits', ['patient_profile_id'])
        op.create_index('ix_visits_date', 'visits', ['visit_date'])

    # ── 7. MEDICAL RECORDS ──
    if not _table_exists('medical_records'):
        op.create_table('medical_records',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False, unique=True),
            sa.Column('record_number', sa.String(30), nullable=False, unique=True),
            sa.Column('chief_complaint', sa.Text(), nullable=True),
            sa.Column('present_illness', sa.Text(), nullable=True),
            sa.Column('past_history', sa.Text(), nullable=True),
            sa.Column('family_history', sa.Text(), nullable=True),
            sa.Column('physical_exam', sa.Text(), nullable=True),
            sa.Column('doctor_note', sa.Text(), nullable=True),
            sa.Column('status', sa.Enum('DRAFT', 'FINAL', name='mr_status_enum'), nullable=False, server_default=sa.text("'DRAFT'")),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_mr_id', 'medical_records', ['id'])
        op.create_index('ix_mr_visit_id', 'medical_records', ['visit_id'], unique=True)
        op.create_index('ix_mr_record_number', 'medical_records', ['record_number'], unique=True)

    # ── 8. SOAP NOTES ──
    if not _table_exists('soap_notes'):
        op.create_table('soap_notes',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False, unique=True),
            sa.Column('subjective', sa.Text(), nullable=True),
            sa.Column('objective', sa.Text(), nullable=True),
            sa.Column('assessment', sa.Text(), nullable=True),
            sa.Column('plan', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_soap_id', 'soap_notes', ['id'])
        op.create_index('ix_soap_visit_id', 'soap_notes', ['visit_id'], unique=True)

    # ── 9. VITAL SIGNS ──
    if not _table_exists('vital_signs'):
        op.create_table('vital_signs',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False, unique=True),
            sa.Column('systolic', sa.Integer(), nullable=True),
            sa.Column('diastolic', sa.Integer(), nullable=True),
            sa.Column('pulse', sa.Integer(), nullable=True),
            sa.Column('respiration', sa.Integer(), nullable=True),
            sa.Column('temperature', sa.DECIMAL(5, 2), nullable=True),
            sa.Column('spo2', sa.DECIMAL(5, 2), nullable=True),
            sa.Column('height', sa.DECIMAL(5, 2), nullable=True),
            sa.Column('weight', sa.DECIMAL(5, 2), nullable=True),
            sa.Column('bmi', sa.DECIMAL(5, 2), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_vs_id', 'vital_signs', ['id'])
        op.create_index('ix_vs_visit_id', 'vital_signs', ['visit_id'], unique=True)

    # ── 10. DIAGNOSES ──
    if not _table_exists('diagnoses'):
        op.create_table('diagnoses',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False),
            sa.Column('icd10_id', sa.String(36), sa.ForeignKey('icd10_codes.id', ondelete='RESTRICT'), nullable=False),
            sa.Column('diagnosis_type', sa.Enum('PRIMARY', 'SECONDARY', name='diagnosis_type_enum'), nullable=False),
            sa.Column('diagnosis_note', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_diag_id', 'diagnoses', ['id'])
        op.create_index('ix_diag_visit_id', 'diagnoses', ['visit_id'])
        op.create_index('ix_diag_icd10_id', 'diagnoses', ['icd10_id'])

    # ── 11. VISIT PROCEDURES ──
    if not _table_exists('visit_procedures'):
        op.create_table('visit_procedures',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False),
            sa.Column('procedure_id', sa.String(36), sa.ForeignKey('medical_procedures.id', ondelete='RESTRICT'), nullable=False),
            sa.Column('notes', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_vp_id', 'visit_procedures', ['id'])
        op.create_index('ix_vp_visit_id', 'visit_procedures', ['visit_id'])
        op.create_index('ix_vp_procedure_id', 'visit_procedures', ['procedure_id'])

    # ── 12. MEDICAL ATTACHMENTS ──
    if not _table_exists('medical_attachments'):
        op.create_table('medical_attachments',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False),
            sa.Column('file_name', sa.String(255), nullable=False),
            sa.Column('file_path', sa.Text(), nullable=False),
            sa.Column('mime_type', sa.String(100), nullable=True),
            sa.Column('uploaded_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_ma_id', 'medical_attachments', ['id'])
        op.create_index('ix_ma_visit_id', 'medical_attachments', ['visit_id'])

    # ── 13. PRESCRIPTIONS ──
    if not _table_exists('prescriptions'):
        op.create_table('prescriptions',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False, unique=True),
            sa.Column('healthcare_professional_id', sa.String(36), sa.ForeignKey('healthcare_professionals.id', ondelete='SET NULL'), nullable=True),
            sa.Column('prescription_date', sa.DateTime(), nullable=False),
            sa.Column('status', sa.Enum('ACTIVE', 'DISPENSED', 'CANCELLED', name='rx_status_enum'), nullable=False, server_default=sa.text("'ACTIVE'")),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_rx_id', 'prescriptions', ['id'])
        op.create_index('ix_rx_visit_id', 'prescriptions', ['visit_id'], unique=True)

    # ── 14. PRESCRIPTION ITEMS ──
    if not _table_exists('prescription_items'):
        op.create_table('prescription_items',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('prescription_id', sa.String(36), sa.ForeignKey('prescriptions.id', ondelete='CASCADE'), nullable=False),
            sa.Column('medicine_id', sa.Integer(), sa.ForeignKey('items.id', ondelete='RESTRICT'), nullable=False),
            sa.Column('dosage', sa.String(100), nullable=True),
            sa.Column('frequency', sa.String(100), nullable=True),
            sa.Column('duration', sa.String(100), nullable=True),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.Column('instruction', sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_rxi_id', 'prescription_items', ['id'])
        op.create_index('ix_rxi_prescription_id', 'prescription_items', ['prescription_id'])
        op.create_index('ix_rxi_medicine_id', 'prescription_items', ['medicine_id'])

    # ── 15. MEDICINE DISPENSES ──
    if not _table_exists('medicine_dispenses'):
        op.create_table('medicine_dispenses',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('prescription_item_id', sa.String(36), sa.ForeignKey('prescription_items.id', ondelete='CASCADE'), nullable=False, unique=True),
            sa.Column('dispensed_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('quantity', sa.Integer(), nullable=False),
            sa.Column('dispensed_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_disp_id', 'medicine_dispenses', ['id'])
        op.create_index('ix_disp_item_id', 'medicine_dispenses', ['prescription_item_id'], unique=True)

    # ── 16. MEDICAL CERTIFICATES ──
    if not _table_exists('medical_certificates'):
        op.create_table('medical_certificates',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('visit_id', sa.String(36), sa.ForeignKey('visits.id', ondelete='CASCADE'), nullable=False),
            sa.Column('certificate_type', sa.Enum('HEALTH', 'SICK', 'FIT_TO_WORK', name='cert_type_enum'), nullable=False),
            sa.Column('start_date', sa.Date(), nullable=False),
            sa.Column('end_date', sa.Date(), nullable=True),
            sa.Column('diagnosis_summary', sa.Text(), nullable=True),
            sa.Column('recommendation', sa.Text(), nullable=True),
            sa.Column('issued_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_cert_id', 'medical_certificates', ['id'])
        op.create_index('ix_cert_visit_id', 'medical_certificates', ['visit_id'])

    # ── 17. CLINIC ACTIVITY LOGS ──
    if not _table_exists('clinic_activity_logs'):
        op.create_table('clinic_activity_logs',
            sa.Column('id', sa.String(36), nullable=False),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
            sa.Column('module', sa.String(50), nullable=False),
            sa.Column('action', sa.String(50), nullable=False),
            sa.Column('table_name', sa.String(50), nullable=True),
            sa.Column('record_id', sa.String(36), nullable=True),
            sa.Column('old_value', sa.JSON(), nullable=True),
            sa.Column('new_value', sa.JSON(), nullable=True),
            sa.Column('ip_address', sa.String(45), nullable=True),
            sa.Column('device', sa.Text(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            mysql_engine='InnoDB',
            mysql_charset='utf8mb4',
        )
        op.create_index('ix_cal_id', 'clinic_activity_logs', ['id'])
        op.create_index('ix_cal_user_id', 'clinic_activity_logs', ['user_id'])
        op.create_index('ix_cal_module', 'clinic_activity_logs', ['module'])


def downgrade() -> None:
    tables = [
        'clinic_activity_logs', 'medicine_dispenses', 'prescription_items',
        'prescriptions', 'medical_attachments', 'visit_procedures',
        'diagnoses', 'vital_signs', 'soap_notes', 'medical_records',
        'visits', 'queues', 'medical_procedures', 'icd10_codes',
        'healthcare_professionals', 'patient_profiles',
    ]
    for t in tables:
        if _table_exists(t):
            op.drop_table(t)
