"""Seed common ICD-10 codes and medical procedures for the clinic module."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DATABASE_URL", "mysql+pymysql://root:@localhost/csms_db")

from sqlalchemy.orm import Session
from app.core.database.session import SessionLocal
from app.modules.clinic.services import icd10_code_service, medical_procedure_service
from app.modules.clinic.schemas import ICD10CodeCreate, MedicalProcedureCreate


COMMON_ICD10_CODES = [
    # A00-B99: Infectious diseases
    ICD10CodeCreate(code="A09", name="Diarrhea and gastroenteritis of presumed infectious origin"),
    ICD10CodeCreate(code="J00", name="Acute nasopharyngitis (common cold)"),
    ICD10CodeCreate(code="J02", name="Acute pharyngitis"),
    ICD10CodeCreate(code="J03", name="Acute tonsillitis"),
    ICD10CodeCreate(code="J06", name="Acute upper respiratory infections of multiple and unspecified sites"),
    # I00-I99: Circulatory system
    ICD10CodeCreate(code="I10", name="Essential (primary) hypertension"),
    ICD10CodeCreate(code="I11", name="Hypertensive heart disease"),
    ICD10CodeCreate(code="I20", name="Angina pectoris"),
    ICD10CodeCreate(code="I48", name="Atrial fibrillation and flutter"),
    ICD10CodeCreate(code="I50", name="Heart failure"),
    # E00-E90: Endocrine/metabolic
    ICD10CodeCreate(code="E10", name="Type 1 diabetes mellitus"),
    ICD10CodeCreate(code="E11", name="Type 2 diabetes mellitus"),
    ICD10CodeCreate(code="E78", name="Disorders of lipoprotein metabolism (dyslipidemia)"),
    # K00-K93: Digestive system
    ICD10CodeCreate(code="K21", name="Gastro-esophageal reflux disease"),
    ICD10CodeCreate(code="K29", name="Gastritis and duodenitis"),
    ICD10CodeCreate(code="K59", name="Constipation"),
    # M00-M99: Musculoskeletal
    ICD10CodeCreate(code="M54", name="Dorsalgia (back pain)"),
    ICD10CodeCreate(code="M79", name="Myalgia / soft tissue disorder"),
    # N00-N99: Genitourinary
    ICD10CodeCreate(code="N39", name="Urinary tract infection"),
    # R00-R99: Symptoms
    ICD10CodeCreate(code="R05", name="Cough"),
    ICD10CodeCreate(code="R06", name="Dyspnea / abnormalities of breathing"),
    ICD10CodeCreate(code="R10", name="Abdominal and pelvic pain"),
    ICD10CodeCreate(code="R11", name="Nausea and vomiting"),
    ICD10CodeCreate(code="R42", name="Dizziness and giddiness"),
    ICD10CodeCreate(code="R50", name="Fever of unknown origin"),
    ICD10CodeCreate(code="R51", name="Headache"),
    # Z00-Z99: Health services
    ICD10CodeCreate(code="Z00", name="General medical examination"),
]


COMMON_MEDICAL_PROCEDURES = [
    MedicalProcedureCreate(code="PHYS_EXAM", name="Complete Physical Examination"),
    MedicalProcedureCreate(code="BLOOD_DRAW", name="Blood Collection / Venipuncture"),
    MedicalProcedureCreate(code="URINALYSIS", name="Urinalysis"),
    MedicalProcedureCreate(code="CBC", name="Complete Blood Count"),
    MedicalProcedureCreate(code="FASTING_GLU", name="Fasting Blood Glucose Test"),
    MedicalProcedureCreate(code="BLOOD_LIPID", name="Lipid Profile"),
    MedicalProcedureCreate(code="LFT", name="Liver Function Test"),
    MedicalProcedureCreate(code="RFT", name="Renal Function Test"),
    MedicalProcedureCreate(code="ECG", name="Electrocardiogram"),
    MedicalProcedureCreate(code="CHEST_XRAY", name="Chest X-Ray"),
    MedicalProcedureCreate(code="ABDOMEN_USG", name="Abdominal Ultrasound"),
    MedicalProcedureCreate(code="WOUND_DRESSING", name="Wound Dressing"),
    MedicalProcedureCreate(code="INJECTION_IV", name="Intravenous Injection"),
    MedicalProcedureCreate(code="INJECTION_IM", name="Intramuscular Injection"),
    MedicalProcedureCreate(code="NEBULIZATION", name="Nebulization Therapy"),
    MedicalProcedureCreate(code="O2_THERAPY", name="Oxygen Therapy"),
    MedicalProcedureCreate(code="BP_CHECK", name="Blood Pressure Monitoring"),
    MedicalProcedureCreate(code="VACCINATION", name="Vaccination / Immunization"),
    MedicalProcedureCreate(code="STITCHES", name="Wound Suturing"),
    MedicalProcedureCreate(code="EAR_IRRIGATION", name="Ear Irrigation"),
]


def seed():
    db: Session = SessionLocal()
    try:
        icd10_count = 0
        for code_data in COMMON_ICD10_CODES:
            existing = icd10_code_service.get_by_code(db, code_data.code)
            if existing is None:
                icd10_code_service.create(db, code_data)
                icd10_count += 1

        proc_count = 0
        for proc_data in COMMON_MEDICAL_PROCEDURES:
            existing = medical_procedure_service.get_all(db, search=proc_data.code, limit=1)
            if not existing:
                medical_procedure_service.create(db, proc_data)
                proc_count += 1

        print(f"Seeded {icd10_count} ICD-10 codes, {proc_count} medical procedures")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
