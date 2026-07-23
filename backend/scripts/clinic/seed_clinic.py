"""Comprehensive seed for Clinic module + supporting data (employees, items).

Run: python -m scripts.clinic.seed_clinic

Dependency order:
  1. Company, Branch, Department, Division, Position, JobLevel
  2. Users → Employees
  3. Categories, Units → Items (medicines)
  4. PatientProfiles, HealthcareProfessionals
  5. ICD10Codes, MedicalProcedures (master data)
  6. Queues, Visits, MedicalRecords, SOAPNotes, VitalSigns
  7. Diagnoses, VisitProcedures
  8. Prescriptions, PrescriptionItems, MedicineDispenses
  9. MedicalCertificates
"""

import sys
import os
from datetime import datetime, date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

os.environ.setdefault("DATABASE_URL", "mysql+pymysql://root:@localhost/csms_db")

from sqlalchemy.orm import Session
from app.core.database.session import SessionLocal
from app.core.auth.password import get_password_hash

from app.models.user import User
from app.models.role import Role
from app.models.item import Item
from app.models.category import Category
from app.models.unit import Unit
from app.core.organization.company.models import Company
from app.core.organization.branch.models import Branch
from app.core.organization.department.models import Department
from app.core.organization.division.models import Division
from app.core.organization.position.models import Position
from app.core.organization.job_level.models import JobLevel
from app.core.organization.employee.models import Employee
from app.core.organization.employee.models import EmploymentStatus, EmploymentType
from app.core.authorization.models import UserRole

from app.modules.clinic.models.patient_profile import PatientProfile, BloodType, Rhesus
from app.modules.clinic.models.healthcare_professional import HealthcareProfessional, Profession, ProfessionalStatus
from app.modules.clinic.models.queue import Queue, QueueStatus
from app.modules.clinic.models.visit import Visit, VisitStatus, VisitType
from app.modules.clinic.models.medical_record import MedicalRecord, MedicalRecordStatus
from app.modules.clinic.models.soap_note import SOAPNote
from app.modules.clinic.models.vital_sign import VitalSign
from app.modules.clinic.models.diagnosis import Diagnosis, DiagnosisType
from app.modules.clinic.models.icd10_code import ICD10Code
from app.modules.clinic.models.medical_procedure import MedicalProcedure
from app.modules.clinic.models.visit_procedure import VisitProcedure
from app.modules.clinic.models.prescription import Prescription, PrescriptionStatus
from app.modules.clinic.models.prescription_item import PrescriptionItem
from app.modules.clinic.models.medicine_dispense import MedicineDispense
from app.modules.clinic.models.medical_certificate import MedicalCertificate, CertificateType


# ════════════════════════════════════════════════════════════════
# HELPER
# ════════════════════════════════════════════════════════════════

def _now():
    return datetime.utcnow()

def _today():
    return date.today()


# ════════════════════════════════════════════════════════════════
# ORGANIZATION DATA
# ════════════════════════════════════════════════════════════════

def seed_organization(db: Session) -> dict:
    out = {}

    # Company
    company = db.query(Company).filter(Company.code == "CSMS").first()
    if not company:
        company = Company(name="Creative Studio Management System", code="CSMS",
                          address="Jl. Contoh No. 123, Jakarta", phone="021-12345678",
                          email="info@csms.com")
        db.add(company)
        db.flush()
        print("  + Company: CSMS")
    out["company"] = company

    # Branch
    branch = db.query(Branch).filter(Branch.code == "HQ").first()
    if not branch:
        branch = Branch(company_id=company.id, name="Headquarters", code="HQ",
                        address="Jl. Contoh No. 123, Jakarta")
        db.add(branch)
        db.flush()
        print("  + Branch: HQ")
    out["branch"] = branch

    # Divisions
    division_names = {"FIN": "Finance", "HRD": "Human Resources", "IT": "Information Technology",
                      "OPS": "Operations", "CLINIC": "Clinic"}
    out["divisions"] = {}
    for code, name in division_names.items():
        div = db.query(Division).filter(Division.name == name).first()
        if not div:
            div = Division(name=name, description=f"{name} Division")
            db.add(div)
            db.flush()
            print(f"  + Division: {name}")
        out["divisions"][code] = div

    # Departments
    dept_list = [
        ("MED", "Medical", "CLINIC"),
        ("NRS", "Nursing", "CLINIC"),
        ("PHARM", "Pharmacy", "CLINIC"),
        ("HR", "Human Resources", "HRD"),
        ("FIN", "Finance", "FIN"),
        ("IT", "Information Technology", "IT"),
        ("OPS", "Operations", "OPS"),
    ]
    out["departments"] = {}
    for code, name, div_key in dept_list:
        dept = db.query(Department).filter(Department.code == code).first()
        if not dept:
            dept = Department(name=name, code=code, description=name)
            db.add(dept)
            db.flush()
            print(f"  + Department: {name}")
        out["departments"][code] = dept

    # Positions
    pos_list = [
        ("DR", "Doctor", "MED"),
        ("NR", "Nurse", "NRS"),
        ("PH", "Pharmacist", "PHARM"),
        ("LB", "Lab Technician", "MED"),
        ("HRM", "HR Manager", "HR"),
        ("FIN", "Finance Staff", "FIN"),
        ("ITS", "IT Staff", "IT"),
        ("OPS", "Operations Staff", "OPS"),
    ]
    out["positions"] = {}
    for code, name, dept_key in pos_list:
        pos = db.query(Position).filter(Position.code == code).first()
        if not pos:
            pos = Position(department_id=out["departments"][dept_key].id, name=name, code=code)
            db.add(pos)
            db.flush()
            print(f"  + Position: {name}")
        out["positions"][code] = pos

    # Job levels
    jl_list = [(1, "Staff"), (2, "Senior Staff"), (3, "Supervisor"), (4, "Manager"), (5, "Director")]
    out["job_levels"] = {}
    for level, name in jl_list:
        code = f"LV{level}"
        jl = db.query(JobLevel).filter(JobLevel.code == code).first()
        if not jl:
            jl = JobLevel(name=name, code=code, level=level)
            db.add(jl)
            db.flush()
            print(f"  + JobLevel: {name}")
        out["job_levels"][code] = jl

    return out


# ════════════════════════════════════════════════════════════════
# USERS & EMPLOYEES
# ════════════════════════════════════════════════════════════════

CLINIC_USERS = [
    {"username": "dr.andini", "email": "dr.andini@csms.com", "full_name": "dr. Andini Putri",
     "profession": Profession.DOCTOR, "license": "SIP-001/DKK/2026",
     "position": "DR", "division": "CLINIC"},
    {"username": "dr.bambang", "email": "dr.bambang@csms.com", "full_name": "dr. Bambang Wijaya",
     "profession": Profession.DOCTOR, "license": "SIP-002/DKK/2026",
     "position": "DR", "division": "CLINIC"},
    {"username": "nurse.citra", "email": "nurse.citra@csms.com", "full_name": "Citra Dewi, S.Kep",
     "profession": Profession.NURSE, "license": "SIP-003/DKK/2026",
     "position": "NR", "division": "CLINIC"},
    {"username": "nurse.dodi", "email": "nurse.dodi@csms.com", "full_name": "Dodi Firmansyah, S.Kep",
     "profession": Profession.NURSE, "license": "SIP-004/DKK/2026",
     "position": "NR", "division": "CLINIC"},
    {"username": "pharma.eka", "email": "pharma.eka@csms.com", "full_name": "Eka Yulianti, S.Farm",
     "profession": Profession.PHARMACIST, "license": "SIP-005/DKK/2026",
     "position": "PH", "division": "CLINIC"},
    {"username": "lab.fajar", "email": "lab.fajar@csms.com", "full_name": "Fajar Pratama, A.Md",
     "profession": Profession.LAB_TECHNICIAN, "license": "SIP-006/DKK/2026",
     "position": "LB", "division": "CLINIC"},
]

PATIENT_EMPLOYEES = [
    {"username": "employee.gita",    "full_name": "Gita Safitri",         "dept": "HR"},
    {"username": "employee.hendra",  "full_name": "Hendra Kusuma",        "dept": "FIN"},
    {"username": "employee.irma",    "full_name": "Irma Suryani",         "dept": "IT"},
    {"username": "employee.joko",    "full_name": "Joko Prasetyo",        "dept": "OPS"},
    {"username": "employee.kartika", "full_name": "Kartika Dewi",         "dept": "FIN"},
    {"username": "employee.leo",     "full_name": "Leo Firmansyah",       "dept": "IT"},
    {"username": "employee.maya",    "full_name": "Maya Anggraini",       "dept": "HR"},
    {"username": "employee.nando",   "full_name": "Nando Pratama",       "dept": "OPS"},
]


def seed_users_and_employees(db: Session, org: dict) -> dict:
    out = {"users": {}, "employees": {}, "hc_pros": []}

    role = db.query(Role).filter(Role.name == "STAFF").first()
    if not role:
        role = Role(name="STAFF", description="Staff")
        db.add(role)
        db.flush()

    emp_num = 1
    for u in CLINIC_USERS:
        user = db.query(User).filter(User.username == u["username"]).first()
        if not user:
            user = User(username=u["username"], email=u["email"],
                        hashed_password=get_password_hash("password123"),
                        is_active=True, is_verified=True, must_change_password=False)
            db.add(user)
            db.flush()
            ur = UserRole(user_id=user.id, role_id=role.id)
            db.add(ur)
            print(f"  + User: {u['username']}")

        emp = db.query(Employee).filter(Employee.user_id == user.id).first()
        if not emp:
            emp_num_str = f"EMP{emp_num:04d}"
            dept_key = "HR" if u["division"] == "CLINIC" else "HR"  # clinic staff in HR dept
            emp = Employee(
                user_id=user.id, employee_number=emp_num_str, full_name=u["full_name"],
                company_id=org["company"].id, branch_id=org["branch"].id,
                department_id=org["departments"]["MED"].id if u["profession"] == Profession.DOCTOR
                          else org["departments"]["NRS"].id if u["profession"] == Profession.NURSE
                          else org["departments"]["PHARM"].id if u["profession"] == Profession.PHARMACIST
                          else org["departments"]["MED"].id,
                position_id=org["positions"]["DR"].id if u["profession"] == Profession.DOCTOR
                           else org["positions"]["NR"].id if u["profession"] == Profession.NURSE
                           else org["positions"]["PH"].id if u["profession"] == Profession.PHARMACIST
                           else org["positions"]["LB"].id,
                division_id=org["divisions"]["CLINIC"].id,
                job_level_id=org["job_levels"]["LV3"].id if u["profession"] == Profession.DOCTOR
                            else org["job_levels"]["LV2"].id,
                employment_status=EmploymentStatus.ACTIVE,
                employment_type=EmploymentType.PERMANENT,
                join_date=date(2024, 1, 1),
            )
            db.add(emp)
            db.flush()
            print(f"  + Employee: {u['full_name']} ({emp_num_str})")
            emp_num += 1

        out["users"][u["username"]] = user
        out["employees"][u["username"]] = emp
        out["hc_pros"].append((emp, u["profession"], u["license"]))

    for p in PATIENT_EMPLOYEES:
        user = db.query(User).filter(User.username == p["username"]).first()
        if not user:
            user = User(username=p["username"], email=f"{p['username']}@csms.com",
                        hashed_password=get_password_hash("password123"),
                        is_active=True, is_verified=True, must_change_password=False)
            db.add(user)
            db.flush()
            ur = UserRole(user_id=user.id, role_id=role.id)
            db.add(ur)
            print(f"  + User: {p['username']}")

        emp = db.query(Employee).filter(Employee.user_id == user.id).first()
        if not emp:
            emp_num_str = f"EMP{emp_num:04d}"
            dept_map = {"HR": "HR", "FIN": "FIN", "IT": "IT", "OPS": "OPS"}
            div_map = {"HR": "HRD", "FIN": "FIN", "IT": "IT", "OPS": "OPS"}
            emp = Employee(
                user_id=user.id, employee_number=emp_num_str, full_name=p["full_name"],
                company_id=org["company"].id, branch_id=org["branch"].id,
                department_id=org["departments"][dept_map[p["dept"]]].id,
                position_id=org["positions"]["FIN"].id if p["dept"] == "FIN"
                           else org["positions"]["HRM"].id if p["dept"] == "HR"
                           else org["positions"]["ITS"].id if p["dept"] == "IT"
                           else org["positions"]["OPS"].id,
                division_id=org["divisions"][div_map[p["dept"]]].id,
                job_level_id=org["job_levels"]["LV1"].id,
                employment_status=EmploymentStatus.ACTIVE,
                employment_type=EmploymentType.PERMANENT,
                join_date=date(2023, 6, 1),
            )
            db.add(emp)
            db.flush()
            print(f"  + Employee: {p['full_name']} ({emp_num_str})")
            emp_num += 1

        out["users"][p["username"]] = user
        out["employees"][p["username"]] = emp

    return out


# ════════════════════════════════════════════════════════════════
# CATEGORIES, UNITS & ITEMS (medicines)
# ════════════════════════════════════════════════════════════════

MEDICINES = [
    {"sku": "MED-PCM",  "name": "Paracetamol 500mg",              "qty": 500, "cat": "Obat Umum",     "unit": "Tablet"},
    {"sku": "MED-IBP",  "name": "Ibuprofen 400mg",                "qty": 300, "cat": "Obat Umum",     "unit": "Tablet"},
    {"sku": "MED-AMX",  "name": "Amoxicillin 500mg",              "qty": 200, "cat": "Antibiotik",    "unit": "Kapsul"},
    {"sku": "MED-CTM",  "name": "Cetirizine 10mg",                "qty": 200, "cat": "Antihistamin",  "unit": "Tablet"},
    {"sku": "MED-OMZ",  "name": "Omeprazole 20mg",                "qty": 150, "cat": "Obat Lambung",  "unit": "Kapsul"},
    {"sku": "MED-RAN",  "name": "Ranitidine 150mg",               "qty": 150, "cat": "Obat Lambung",  "unit": "Tablet"},
    {"sku": "MED-SAL",  "name": "Salbutamol Inhaler 100mcg",      "qty": 50,  "cat": "Obat Nafas",    "unit": "Inhaler"},
    {"sku": "MED-DEX",  "name": "Dexamethasone 0.5mg",            "qty": 100, "cat": "Kortikosteroid","unit": "Tablet"},
    {"sku": "MED-CPD",  "name": "Ciprofloxacin 500mg",            "qty": 100, "cat": "Antibiotik",    "unit": "Tablet"},
    {"sku": "MED-MTF",  "name": "Metformin 500mg",                "qty": 200, "cat": "Diabetes",      "unit": "Tablet"},
    {"sku": "MED-AMLP", "name": "Amlodipine 5mg",                 "qty": 200, "cat": "Hipertensi",    "unit": "Tablet"},
    {"sku": "MED-SIM",  "name": "Simvastatin 10mg",               "qty": 150, "cat": "Kolesterol",    "unit": "Tablet"},
    {"sku": "MED-VB1",  "name": "Vitamin B Complex",              "qty": 300, "cat": "Vitamin",       "unit": "Tablet"},
    {"sku": "MED-VC",   "name": "Vitamin C 500mg",                "qty": 400, "cat": "Vitamin",       "unit": "Tablet"},
    {"sku": "MED-ORS",  "name": "Oralit (ORS)",                   "qty": 500, "cat": "Obat Umum",     "unit": "Sachet"},
    {"sku": "MED-CTG",  "name": "CTM (Chlorpheniramine) 4mg",     "qty": 200, "cat": "Antihistamin",  "unit": "Tablet"},
    {"sku": "MED-ASM",  "name": "Asam Mefenamat 500mg",           "qty": 150, "cat": "Obat Umum",     "unit": "Tablet"},
    {"sku": "MED-GLIS", "name": "Gliseril Guaiakolat 100mg",      "qty": 100, "cat": "Obat Batuk",    "unit": "Tablet"},
    {"sku": "MED-B1",   "name": "B1 (Thiamine) 50mg",             "qty": 100, "cat": "Vitamin",       "unit": "Tablet"},
    {"sku": "MED-B6",   "name": "B6 (Pyridoxine) 10mg",           "qty": 100, "cat": "Vitamin",       "unit": "Tablet"},
]


def seed_items(db: Session) -> dict:
    out = {"items": {}}

    for m in MEDICINES:
        cat = db.query(Category).filter(Category.name == m["cat"]).first()
        if not cat:
            cat = Category(name=m["cat"])
            db.add(cat)
            db.flush()

        unit = db.query(Unit).filter(Unit.name == m["unit"]).first()
        if not unit:
            unit = Unit(name=m["unit"])
            db.add(unit)
            db.flush()

        item = db.query(Item).filter(Item.sku == m["sku"]).first()
        if not item:
            item = Item(sku=m["sku"], name=m["name"], stock_qty=m["qty"],
                        is_active=True, category_id=cat.id, unit_id=unit.id)
            db.add(item)
            db.flush()
            print(f"  + Item: {m['name']} ({m['sku']})")

        out["items"][m["sku"]] = item

    return out


# ════════════════════════════════════════════════════════════════
# PATIENT PROFILES
# ════════════════════════════════════════════════════════════════

PATIENT_DATA = [
    {"emp": "employee.gita",    "mr": "RM-001", "blood": BloodType.A,  "rhesus": Rhesus.POSITIVE, "allergy": "Dust"},
    {"emp": "employee.hendra",  "mr": "RM-002", "blood": BloodType.B,  "rhesus": Rhesus.POSITIVE, "allergy": None},
    {"emp": "employee.irma",    "mr": "RM-003", "blood": BloodType.O,  "rhesus": Rhesus.POSITIVE, "allergy": "Seafood"},
    {"emp": "employee.joko",    "mr": "RM-004", "blood": BloodType.AB, "rhesus": Rhesus.NEGATIVE, "allergy": None},
    {"emp": "employee.kartika", "mr": "RM-005", "blood": BloodType.O,  "rhesus": Rhesus.POSITIVE, "allergy": "Penicillin"},
    {"emp": "employee.leo",     "mr": "RM-006", "blood": BloodType.A,  "rhesus": Rhesus.POSITIVE, "allergy": None},
    {"emp": "employee.maya",    "mr": "RM-007", "blood": BloodType.B,  "rhesus": Rhesus.NEGATIVE, "allergy": None},
    {"emp": "employee.nando",   "mr": "RM-008", "blood": BloodType.O,  "rhesus": Rhesus.POSITIVE, "allergy": "Latex"},
]


def seed_patient_profiles(db: Session, employees: dict) -> list:
    profiles = []
    for p in PATIENT_DATA:
        emp = employees[p["emp"]]
        exists = db.query(PatientProfile).filter(PatientProfile.employee_id == emp.id).first()
        if not exists:
            pp = PatientProfile(
                employee_id=emp.id,
                medical_record_number=p["mr"],
                blood_type=p["blood"],
                rhesus=p["rhesus"],
                allergy_note=p["allergy"],
                emergency_contact_name="Emergency Contact",
                emergency_contact_phone="08123456789",
            )
            db.add(pp)
            db.flush()
            print(f"  + PatientProfile: {p['mr']} ({p['emp']})")
            profiles.append(pp)
        else:
            profiles.append(exists)
    return profiles


# ════════════════════════════════════════════════════════════════
# HEALTHCARE PROFESSIONALS
# ════════════════════════════════════════════════════════════════

def seed_hc_professionals(db: Session, hc_pros_input: list) -> dict:
    mapping = {}
    for emp, profession, license_num in hc_pros_input:
        exists = db.query(HealthcareProfessional).filter(
            HealthcareProfessional.employee_id == emp.id
        ).first()
        if not exists:
            hcp = HealthcareProfessional(
                employee_id=emp.id,
                profession=profession,
                license_number=license_num,
                specialization="General" if profession == Profession.DOCTOR else None,
                status=ProfessionalStatus.ACTIVE,
            )
            db.add(hcp)
            db.flush()
            print(f"  + HCProfessional: {emp.full_name} ({profession.value})")
            mapping[emp.full_name] = hcp
        else:
            mapping[emp.full_name] = exists
    return mapping


# ════════════════════════════════════════════════════════════════
# ICD-10 CODES (reuse data from seed_icd10)
# ════════════════════════════════════════════════════════════════

COMMON_ICD10 = [
    ("A09", "Diarrhea and gastroenteritis of presumed infectious origin"),
    ("J00", "Acute nasopharyngitis (common cold)"),
    ("J02", "Acute pharyngitis"),
    ("J03", "Acute tonsillitis"),
    ("J06", "Acute upper respiratory infections of multiple and unspecified sites"),
    ("I10", "Essential (primary) hypertension"),
    ("I11", "Hypertensive heart disease"),
    ("I20", "Angina pectoris"),
    ("I48", "Atrial fibrillation and flutter"),
    ("I50", "Heart failure"),
    ("E10", "Type 1 diabetes mellitus"),
    ("E11", "Type 2 diabetes mellitus"),
    ("E78", "Disorders of lipoprotein metabolism (dyslipidemia)"),
    ("K21", "Gastro-esophageal reflux disease"),
    ("K29", "Gastritis and duodenitis"),
    ("K59", "Constipation"),
    ("M54", "Dorsalgia (back pain)"),
    ("M79", "Myalgia / soft tissue disorder"),
    ("N39", "Urinary tract infection"),
    ("R05", "Cough"),
    ("R06", "Dyspnea / abnormalities of breathing"),
    ("R10", "Abdominal and pelvic pain"),
    ("R11", "Nausea and vomiting"),
    ("R42", "Dizziness and giddiness"),
    ("R50", "Fever of unknown origin"),
    ("R51", "Headache"),
    ("Z00", "General medical examination"),
]


def seed_icd10(db: Session) -> dict:
    codes = {}
    for code, name in COMMON_ICD10:
        existing = db.query(ICD10Code).filter(ICD10Code.code == code).first()
        if not existing:
            existing = ICD10Code(code=code, name=name)
            db.add(existing)
            db.flush()
        codes[code] = existing
    print(f"  + ICD10Codes: {len(codes)} codes")
    return codes


# ════════════════════════════════════════════════════════════════
# MEDICAL PROCEDURES
# ════════════════════════════════════════════════════════════════

COMMON_PROCEDURES = [
    ("PHYS_EXAM", "Complete Physical Examination"),
    ("BLOOD_DRAW", "Blood Collection / Venipuncture"),
    ("URINALYSIS", "Urinalysis"),
    ("CBC", "Complete Blood Count"),
    ("FASTING_GLU", "Fasting Blood Glucose Test"),
    ("ECG", "Electrocardiogram"),
    ("CHEST_XRAY", "Chest X-Ray"),
    ("WOUND_DRESSING", "Wound Dressing"),
    ("INJECTION_IV", "Intravenous Injection"),
    ("INJECTION_IM", "Intramuscular Injection"),
    ("NEBULIZATION", "Nebulization Therapy"),
    ("STITCHES", "Wound Suturing"),
]


def seed_procedures(db: Session) -> dict:
    procs = {}
    for code, name in COMMON_PROCEDURES:
        existing = db.query(MedicalProcedure).filter(MedicalProcedure.code == code).first()
        if not existing:
            existing = MedicalProcedure(code=code, name=name)
            db.add(existing)
            db.flush()
        procs[code] = existing
    print(f"  + MedicalProcedures: {len(procs)} procedures")
    return procs


# ════════════════════════════════════════════════════════════════
# VISIT DATA (creates visits + all related entities)
# ════════════════════════════════════════════════════════════════

VISIT_TEMPLATES = [
    # (patient_emp_key, doctor_name, visit_type, complaint, diagnosis_icd10, procedures, medicines)
    {
        "patient": "employee.gita",
        "doctor": "dr. Andini Putri",
        "type": VisitType.REGULAR,
        "complaint": "Demam dan batuk sejak 3 hari",
        "soap": {
            "subjective": "Pasien mengeluh demam sejak 3 hari, batuk berdahak, pilek. Nyeri tenggorokan saat menelan.",
            "objective": "TD 120/80, N 88, RR 20, T 38.2°C. Tampak hiperemis pada faring. Auskultasi paru: rhonchi +/+, wheezing -/-.",
            "assessment": "ISPA akut dengan faringitis.",
            "plan": "Terapi simptomatik. Istirahat cukup. Kontrol bila demam >3 hari.",
        },
        "vital": {"systolic": 120, "diastolic": 80, "pulse": 88, "respiration": 20, "temperature": 38.2, "spo2": 97.0, "height": 160, "weight": 55},
        "diagnoses": [("J02", DiagnosisType.PRIMARY)],
        "procedures": ["PHYS_EXAM"],
        "medicines": [("MED-PCM", "3x1", "1 tablet", "3 hari", 9, "Setelah makan"), ("MED-CTG", "3x1", "1 tablet", "3 hari", 9, "Malam hari")],
        "cert": None,
    },
    {
        "patient": "employee.hendra",
        "doctor": "dr. Bambang Wijaya",
        "type": VisitType.REGULAR,
        "complaint": "Nyeri ulu hati dan perut kembung",
        "soap": {
            "subjective": "Nyeri epigastrium sejak 1 minggu, terutama setelah makan. Sering sendawa, perut terasa penuh.",
            "objective": "TD 130/85, N 76, RR 18, T 36.6°C. Abdomen: supel, nyeri tekan epigastrium +, hepar/lien tidak teraba. Bising usus normal.",
            "assessment": "Dyspepsia syndrome. Suspect gastritis.",
            "plan": "Pemberian antasida. Konsultasi gizi. Hindari makanan pedas dan berlemak.",
        },
        "vital": {"systolic": 130, "diastolic": 85, "pulse": 76, "respiration": 18, "temperature": 36.6, "spo2": 98.0, "height": 170, "weight": 75},
        "diagnoses": [("K29", DiagnosisType.PRIMARY)],
        "procedures": ["PHYS_EXAM"],
        "medicines": [("MED-OMZ", "2x1", "1 kapsul", "14 hari", 28, "Sebelum makan"), ("MED-RAN", "2x1", "1 tablet", "7 hari", 14, "Setelah makan")],
        "cert": {"type": CertificateType.SICK, "days": 2, "reason": "Gastritis akut, perlu istirahat"},
    },
    {
        "patient": "employee.irma",
        "doctor": "dr. Andini Putri",
        "type": VisitType.REGULAR,
        "complaint": "Sakit kepala hebat dan pusing berputar",
        "soap": {
            "subjective": "Sakit kepala sejak 2 hari, berat, terutama di daerah frontal. Pusing berputar saat mengubah posisi. Mual.",
            "objective": "TD 110/70, N 82, RR 18, T 36.5°C. Pupil isokor, reflek cahaya +/+. Nyeri tekan area frontal +. Tanda vital lain normal.",
            "assessment": "Tension type headache dengan vertigo.",
            "plan": "Analgesik. Istirahat. Hindari stres. Kontrol bila tidak membaik.",
        },
        "vital": {"systolic": 110, "diastolic": 70, "pulse": 82, "respiration": 18, "temperature": 36.5, "spo2": 99.0, "height": 155, "weight": 50},
        "diagnoses": [("R51", DiagnosisType.PRIMARY), ("R42", DiagnosisType.SECONDARY)],
        "procedures": ["PHYS_EXAM"],
        "medicines": [("MED-IBP", "3x1", "1 tablet", "3 hari", 9, "Setelah makan")],
        "cert": None,
    },
    {
        "patient": "employee.joko",
        "doctor": "dr. Bambang Wijaya",
        "type": VisitType.EMERGENCY,
        "complaint": "Luka iris di jari telunjuk kanan akibat terpotong kertas",
        "soap": {
            "subjective": "Terpotong kertas saat bekerja. Luka cukup dalam, perdarahan aktif.",
            "objective": "TD 125/80, N 90, RR 20, T 36.8°C. Luka iris transversal pada jari telunjuk kanan, panjang ± 2cm, dalam ± 0.5cm. Tidak ada tanda infeksi. CRT <2 detik.",
            "assessment": "Vulnus scissum digiti II dextri.",
            "plan": "Bersihkan luka, jahit, berikan antibiotik profilaksis. TT update.",
        },
        "vital": {"systolic": 125, "diastolic": 80, "pulse": 90, "respiration": 20, "temperature": 36.8, "spo2": 98.0, "height": 175, "weight": 70},
        "diagnoses": [("M79", DiagnosisType.PRIMARY)],
        "procedures": ["STITCHES", "WOUND_DRESSING"],
        "medicines": [("MED-AMX", "3x1", "1 kapsul", "5 hari", 15, "Setelah makan"), ("MED-IBP", "3x1", "1 tablet", "3 hari", 9, "Setelah makan")],
        "cert": None,
    },
    {
        "patient": "employee.kartika",
        "doctor": "dr. Andini Putri",
        "type": VisitType.FOLLOW_UP,
        "complaint": "Kontrol tekanan darah",
        "soap": {
            "subjective": "Pasien hipertensi rutin kontrol. Keluhan pusing sudah berkurang. Obat rutin diminum teratur.",
            "objective": "TD 135/85, N 80, RR 18, T 36.5°C. Jantung: S1S2 reguler, murmur -/-. Paru: vesikuler +/+.",
            "assessment": "Hipertensi stage 1 terkontrol.",
            "plan": "Lanjutkan terapi. Diet rendah garam. Olahraga teratur. Kontrol 1 bulan lagi.",
        },
        "vital": {"systolic": 135, "diastolic": 85, "pulse": 80, "respiration": 18, "temperature": 36.5, "spo2": 99.0, "height": 165, "weight": 60},
        "diagnoses": [("I10", DiagnosisType.PRIMARY)],
        "procedures": ["PHYS_EXAM", "ECG"],
        "medicines": [("MED-AMLP", "1x1", "1 tablet", "30 hari", 30, "Pagi hari")],
        "cert": None,
    },
    {
        "patient": "employee.leo",
        "doctor": "dr. Bambang Wijaya",
        "type": VisitType.REGULAR,
        "complaint": "Batuk berdahak sejak 5 hari, sesak napas",
        "soap": {
            "subjective": "Batuk berdahak hijau, sesak terutama saat malam hari. Riwayat asma.",
            "objective": "TD 118/75, N 92, RR 22, T 37.5°C. Auskultasi: wheezing +/+, rhonchi +/+. SpO2 95%.",
            "assessment": "Eksaserbasi asma bronkial + ISPA.",
            "plan": "Nebulisasi salbutamol. Antibiotik. Kortikosteroid jangka pendek.",
        },
        "vital": {"systolic": 118, "diastolic": 75, "pulse": 92, "respiration": 22, "temperature": 37.5, "spo2": 95.0, "height": 172, "weight": 68},
        "diagnoses": [("J06", DiagnosisType.PRIMARY)],
        "procedures": ["NEBULIZATION", "PHYS_EXAM"],
        "medicines": [("MED-SAL", "Sesuai gejala", "2 puff", "7 hari", 1, "Saat sesak"), ("MED-DEX", "3x1", "1 tablet", "5 hari", 15, "Setelah makan"), ("MED-AMX", "3x1", "1 kapsul", "5 hari", 15, "Setelah makan")],
        "cert": {"type": CertificateType.SICK, "days": 3, "reason": "Eksaserbasi asma, perlu rawat jalan dan istirahat"},
    },
    {
        "patient": "employee.maya",
        "doctor": "dr. Andini Putri",
        "type": VisitType.REGULAR,
        "complaint": "Nyeri pinggang bawah sejak 3 hari",
        "soap": {
            "subjective": "Nyeri di daerah pinggang bawah, menjalar ke paha kanan. Sulit duduk lama. Riwayat kerja duduk >8 jam/hari.",
            "objective": "TD 120/80, N 78, RR 18, T 36.6°C. Nyeri tekan area L4-L5 +. Straight leg raise test (+). Kekuatan otot 5/5.",
            "assessment": "Low back pain mekanik, suspected HNP ringan.",
            "plan": "Analgesik. Fisioterapi. Perbaiki postur kerja. Kursi ergonomis.",
        },
        "vital": {"systolic": 120, "diastolic": 80, "pulse": 78, "respiration": 18, "temperature": 36.6, "spo2": 99.0, "height": 158, "weight": 52},
        "diagnoses": [("M54", DiagnosisType.PRIMARY)],
        "procedures": ["PHYS_EXAM"],
        "medicines": [("MED-ASM", "3x1", "1 tablet", "5 hari", 15, "Setelah makan"), ("MED-VB1", "1x1", "1 tablet", "30 hari", 30, "")],
        "cert": None,
    },
    {
        "patient": "employee.nando",
        "doctor": "dr. Bambang Wijaya",
        "type": VisitType.REGULAR,
        "complaint": "Sakit perut dan diare sejak 2 hari",
        "soap": {
            "subjective": "Diare cair 5-6x/hari, sakit perut melilit. Mual. Riwayat makan di kantin 2 hari lalu.",
            "objective": "TD 110/70, N 96, RR 20, T 37.8°C. Abdomen: distensi -, nyeri tekan periumbilikal +. Bising usus meningkat.",
            "assessment": "Gastroenteritis akut, dehidrasi ringan.",
            "plan": "Oralit. Antibiotik jika perlu. Diet lunak. Konsultasi gizi.",
        },
        "vital": {"systolic": 110, "diastolic": 70, "pulse": 96, "respiration": 20, "temperature": 37.8, "spo2": 97.0, "height": 168, "weight": 62},
        "diagnoses": [("A09", DiagnosisType.PRIMARY)],
        "procedures": ["PHYS_EXAM"],
        "medicines": [("MED-ORS", "3x1", "1 sachet", "3 hari", 9, "Larutkan dalam 200ml air"), ("MED-CTM", "1x1", "1 tablet", "3 hari", 3, "Malam hari")],
        "cert": {"type": CertificateType.SICK, "days": 1, "reason": "Gastroenteritis akut, perlu istirahat"},
    },
]


def seed_visits(db: Session, patient_profiles: list, hc_pros: dict, icd10_codes: dict,
                procedures: dict, items: dict, admin_user) -> None:
    today = _today()
    visit_count = db.query(Visit).count()

    patient_by_username = {}
    for p_data, pp in zip(PATIENT_DATA, patient_profiles):
        patient_by_username[p_data["emp"]] = pp
    patient_name = {p["username"]: p["full_name"] for p in PATIENT_EMPLOYEES}

    for idx, tpl in enumerate(VISIT_TEMPLATES):
        patient = patient_by_username.get(tpl["patient"])
        if not patient:
            continue

        doctor = hc_pros.get(tpl["doctor"])
        if not doctor:
            continue

        visit_num = visit_count + idx + 1
        visit_number = f"{today.strftime('%Y%m%d')}{visit_num:04d}"
        visit_date = _now() - timedelta(hours=idx * 2)

        # Queue
        queue = Queue(
            queue_number=f"A{visit_num:03d}",
            queue_date=today,
            status=QueueStatus.FINISHED if tpl["type"] != VisitType.EMERGENCY else QueueStatus.FINISHED,
            called_at=visit_date,
            finished_at=visit_date + timedelta(minutes=30),
        )
        db.add(queue)
        db.flush()

        # Visit
        visit = Visit(
            visit_number=visit_number,
            patient_profile_id=patient.id,
            queue_id=queue.id,
            healthcare_professional_id=doctor.id,
            visit_type=tpl["type"],
            visit_date=visit_date,
            complaint=tpl["complaint"],
            visit_status=VisitStatus.FINISHED,
        )
        db.add(visit)
        db.flush()

        # Medical Record
        mr = MedicalRecord(
            visit_id=visit.id,
            record_number=f"MR-{visit_number}",
            chief_complaint=tpl["complaint"],
            present_illness=tpl["soap"]["subjective"],
            physical_exam=tpl["soap"]["objective"],
            doctor_note=tpl["soap"]["plan"],
            status=MedicalRecordStatus.FINAL,
        )
        db.add(mr)

        # SOAP Note
        soap = SOAPNote(
            visit_id=visit.id,
            subjective=tpl["soap"]["subjective"],
            objective=tpl["soap"]["objective"],
            assessment=tpl["soap"]["assessment"],
            plan=tpl["soap"]["plan"],
        )
        db.add(soap)

        # Vital Sign
        vs = VitalSign(
            visit_id=visit.id,
            systolic=tpl["vital"]["systolic"],
            diastolic=tpl["vital"]["diastolic"],
            pulse=tpl["vital"]["pulse"],
            respiration=tpl["vital"]["respiration"],
            temperature=tpl["vital"]["temperature"],
            spo2=tpl["vital"]["spo2"],
            height=tpl["vital"]["height"],
            weight=tpl["vital"]["weight"],
            bmi=round(tpl["vital"]["weight"] / ((tpl["vital"]["height"] / 100) ** 2), 2),
        )
        db.add(vs)

        # Diagnoses
        diag_order = 0
        for icd10_code, diag_type in tpl["diagnoses"]:
            icd = icd10_codes.get(icd10_code)
            if icd:
                diag = Diagnosis(
                    visit_id=visit.id,
                    icd10_id=icd.id,
                    diagnosis_type=diag_type,
                    diagnosis_note=f"Diagnosis {icd10_code} - {diag_type.value}",
                )
                db.add(diag)
                diag_order += 1

        # Visit Procedures
        for proc_code in tpl["procedures"]:
            proc = procedures.get(proc_code)
            if proc:
                vp = VisitProcedure(
                    visit_id=visit.id,
                    procedure_id=proc.id,
                    notes=f"Prosedur {proc.name}",
                )
                db.add(vp)

        # Prescription
        if tpl["medicines"]:
            rx = Prescription(
                visit_id=visit.id,
                healthcare_professional_id=doctor.id,
                prescription_date=visit_date,
                status=PrescriptionStatus.DISPENSED if tpl["type"] != VisitType.EMERGENCY else PrescriptionStatus.ACTIVE,
            )
            db.add(rx)
            db.flush()

            for med_sku, freq, dosage, duration, qty, instruction in tpl["medicines"]:
                med_item = items.get(med_sku)
                if med_item:
                    rxi = PrescriptionItem(
                        prescription_id=rx.id,
                        medicine_id=med_item.id,
                        dosage=dosage,
                        frequency=freq,
                        duration=duration,
                        quantity=qty,
                        instruction=instruction,
                    )
                    db.add(rxi)
                    db.flush()

                    # Dispense for non-emergency
                    if tpl["type"] != VisitType.EMERGENCY:
                        disp = MedicineDispense(
                            prescription_item_id=rxi.id,
                            dispensed_by=admin_user.id if admin_user else None,
                            quantity=qty,
                            dispensed_at=visit_date + timedelta(minutes=15),
                        )
                        db.add(disp)

        # Medical Certificate
        if tpl["cert"]:
            cert = MedicalCertificate(
                visit_id=visit.id,
                certificate_type=tpl["cert"]["type"],
                start_date=today,
                end_date=today + timedelta(days=tpl["cert"]["days"]),
                diagnosis_summary=tpl["cert"]["reason"],
                recommendation="Istirahat total di rumah",
                issued_by=admin_user.id if admin_user else None,
            )
            db.add(cert)

        print(f"  + Visit: {visit_number} ({patient_name[tpl['patient']]} → {tpl['doctor']})")

    db.flush()


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def seed_all():
    db = SessionLocal()
    try:
        print("\n=== CLINIC SEED ===\n")

        print("[1/9] Organization...")
        org = seed_organization(db)

        print("[2/9] Users & Employees...")
        emp_data = seed_users_and_employees(db, org)

        print("[3/9] Categories, Units & Items (medicines)...")
        item_data = seed_items(db)

        print("[4/9] ICD-10 Codes...")
        icd10_codes = seed_icd10(db)

        print("[5/9] Medical Procedures...")
        procedures = seed_procedures(db)

        print("[6/9] Patient Profiles...")
        patient_profiles = seed_patient_profiles(db, emp_data["employees"])

        print("[7/9] Healthcare Professionals...")
        hc_pros = seed_hc_professionals(db, emp_data["hc_pros"])

        print("[8/9] Visits + Records + Prescriptions...")
        admin_user = db.query(User).filter(User.username == "dr.andini").first()
        seed_visits(db, patient_profiles, hc_pros, icd10_codes,
                    procedures, item_data["items"], admin_user)

        print("[9/9] Committing...")
        db.commit()

        print(f"\n{'='*50}")
        print("SEED COMPLETED SUCCESSFULLY")
        print(f"  Organization: 1 company, 1 branch, {len(org['divisions'])} divisions, 6 departments")
        print(f"  Users: {len(emp_data['users'])}")
        print(f"  Employees: {len(emp_data['employees'])}")
        print(f"  Items (meds): {len(item_data['items'])}")
        print(f"  ICD-10 Codes: {len(icd10_codes)}")
        print(f"  Procedures: {len(procedures)}")
        print(f"  Patient Profiles: {len(patient_profiles)}")
        print(f"  HC Professionals: {len(hc_pros)}")
        print(f"  Visits: {len(VISIT_TEMPLATES)}")
        print(f"{'='*50}\n")

    except Exception as e:
        db.rollback()
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
