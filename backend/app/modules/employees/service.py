from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.core.exceptions import CSMSException
from app.core.organization.employee.models import Employee
from app.core.organization.employee.service import employee_core_service
from app.core.organization.employee.schemas import EmployeeCreate as CoreEmployeeCreate
from app.core.organization.employee_contact.models import EmployeeContact
from app.core.organization.employee_education.models import EmployeeEducation
from app.core.organization.employee_bank.models import EmployeeBank
from app.core.organization.employee_emergency_contact.models import EmployeeEmergencyContact
from app.core.organization.employee_family.models import EmployeeFamily
from app.core.organization.bank.models import Bank
from app.models.user import User
from app.modules.employees.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse


class EmployeeService:

    def _build_response(self, emp: Employee) -> EmployeeResponse:
        user = emp.user
        contacts = emp.contacts
        educations = emp.educations
        banks = emp.banks
        emergency_contacts = emp.emergency_contacts

        primary_contact = None
        if contacts:
            for c in contacts:
                if c.is_primary:
                    primary_contact = c
                    break
            if not primary_contact:
                primary_contact = contacts[0]

        highest_edu = None
        if educations:
            for e in educations:
                if e.is_highest or highest_edu is None:
                    highest_edu = e

        primary_bank = banks[0] if banks else None
        primary_emergency = emergency_contacts[0] if emergency_contacts else None

        resp = EmployeeResponse(
            id=emp.id,
            user_id=emp.user_id,
            employee_number=emp.employee_number,
            full_name=emp.full_name,
            username=user.username if user else None,
            email=user.email if user else None,
            company_id=emp.company_id,
            company_name=emp.company.name if emp.company else None,
            branch_id=emp.branch_id,
            branch_name=emp.branch.name if emp.branch else None,
            department_id=emp.department_id,
            department_name=emp.department.name if emp.department else None,
            position_id=emp.position_id,
            position_name=emp.position.name if emp.position else None,
            division_id=emp.division_id,
            division_name=emp.division.name if emp.division else None,
            job_level_id=emp.job_level_id,
            job_level_name=emp.job_level.name if emp.job_level else None,
            employment_status=emp.employment_status,
            employment_type=emp.employment_type,
            join_date=emp.join_date,
            deleted_at=emp.deleted_at.isoformat() if emp.deleted_at else None,
        )

        if primary_contact:
            resp.phone = primary_contact.phone
            resp.alternate_phone = primary_contact.alternate_phone
            resp.current_address = primary_contact.current_address
            resp.current_province = primary_contact.current_province
            resp.current_city = primary_contact.current_city
            resp.current_district = primary_contact.current_district
            resp.current_postal_code = primary_contact.current_postal_code
            resp.permanent_address = primary_contact.permanent_address
            resp.permanent_province = primary_contact.permanent_province
            resp.permanent_city = primary_contact.permanent_city
            resp.permanent_district = primary_contact.permanent_district
            resp.permanent_postal_code = primary_contact.permanent_postal_code

        if highest_edu:
            resp.education_level = highest_edu.level
            resp.education_institution = highest_edu.institution
            resp.education_major = highest_edu.major
            resp.education_start_year = highest_edu.start_year
            resp.education_end_year = highest_edu.end_year
            resp.education_graduation_year = highest_edu.graduation_year
            resp.education_certificate_number = highest_edu.certificate_number
            resp.education_graduated = highest_edu.graduated

        if primary_bank:
            resp.bank_id = primary_bank.bank_id
            resp.bank_name = primary_bank.bank.name if primary_bank.bank else None
            resp.bank_account = primary_bank.account_number
            resp.bank_account_holder = primary_bank.account_holder

        if primary_emergency:
            resp.emergency_contact_name = primary_emergency.name
            resp.emergency_contact_phone = primary_emergency.phone
            resp.emergency_contact_relationship = primary_emergency.relation

        return resp

    def get_all(
        self,
        db: Session,
        branch_id: Optional[int] = None,
        department_id: Optional[int] = None,
        position_id: Optional[int] = None,
        division_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[List[EmployeeResponse], int]:
        query = (
            db.query(Employee)
            .options(
                joinedload(Employee.user),
                joinedload(Employee.company),
                joinedload(Employee.branch),
                joinedload(Employee.department),
                joinedload(Employee.position),
                joinedload(Employee.division),
                joinedload(Employee.job_level),
                joinedload(Employee.contacts),
                joinedload(Employee.educations),
                joinedload(Employee.banks),
                joinedload(Employee.banks).joinedload(EmployeeBank.bank),
                joinedload(Employee.emergency_contacts),
            )
        )
        if branch_id:
            query = query.filter(Employee.branch_id == branch_id)
        if department_id:
            query = query.filter(Employee.department_id == department_id)
        if position_id:
            query = query.filter(Employee.position_id == position_id)
        if division_id:
            query = query.filter(Employee.division_id == division_id)

        query = query.filter(Employee.deleted_at.is_(None))

        total = query.count()
        employees = query.order_by(Employee.employee_number).offset(skip).limit(limit).all()

        return [self._build_response(emp) for emp in employees], total

    def get_by_id(self, db: Session, employee_id: int) -> EmployeeResponse:
        emp = (
            db.query(Employee)
            .options(
                joinedload(Employee.user),
                joinedload(Employee.company),
                joinedload(Employee.branch),
                joinedload(Employee.department),
                joinedload(Employee.position),
                joinedload(Employee.division),
                joinedload(Employee.job_level),
                joinedload(Employee.contacts),
                joinedload(Employee.educations),
                joinedload(Employee.banks),
                joinedload(Employee.banks).joinedload(EmployeeBank.bank),
                joinedload(Employee.emergency_contacts),
            )
            .filter(Employee.id == employee_id, Employee.deleted_at.is_(None))
            .first()
        )
        if not emp:
            raise CSMSException("Employee not found", status_code=404)
        return self._build_response(emp)

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[EmployeeResponse]:
        emp = (
            db.query(Employee)
            .options(
                joinedload(Employee.user),
                joinedload(Employee.company),
                joinedload(Employee.branch),
                joinedload(Employee.department),
                joinedload(Employee.position),
                joinedload(Employee.division),
                joinedload(Employee.job_level),
                joinedload(Employee.contacts),
                joinedload(Employee.educations),
                joinedload(Employee.banks),
                joinedload(Employee.banks).joinedload(EmployeeBank.bank),
                joinedload(Employee.emergency_contacts),
            )
            .filter(Employee.user_id == user_id, Employee.deleted_at.is_(None))
            .first()
        )
        if not emp:
            return None
        return self._build_response(emp)

    def create(self, db: Session, data: EmployeeCreate) -> EmployeeResponse:
        existing = employee_core_service.get_by_employee_number(db, data.employee_number)
        if existing:
            raise CSMSException(
                f"Employee with number '{data.employee_number}' already exists", status_code=409
            )
        existing = employee_core_service.get_by_user_id(db, data.user_id)
        if existing:
            raise CSMSException(
                f"User {data.user_id} is already linked to employee {existing.employee_number}",
                status_code=409,
            )

        core_data = CoreEmployeeCreate(
            user_id=data.user_id,
            employee_number=data.employee_number,
            full_name=data.full_name,
            company_id=data.company_id,
            branch_id=data.branch_id,
            department_id=data.department_id,
            position_id=data.position_id,
            division_id=data.division_id,
            job_level_id=data.job_level_id,
            employment_status=data.employment_status,
            employment_type=data.employment_type,
            join_date=data.join_date,
        )
        emp = employee_core_service.create(db, core_data)

        has_contact_data = any([
            data.phone, data.current_address, data.permanent_address,
            data.current_province, data.current_city
        ])
        if has_contact_data:
            db.add(EmployeeContact(
                employee_id=emp.id,
                contact_type="primary",
                is_primary=True,
                phone=data.phone,
                alternate_phone=data.alternate_phone,
                current_address=data.current_address,
                current_province=data.current_province,
                current_city=data.current_city,
                current_district=data.current_district,
                current_postal_code=data.current_postal_code,
                permanent_address=data.permanent_address,
                permanent_province=data.permanent_province,
                permanent_city=data.permanent_city,
                permanent_district=data.permanent_district,
                permanent_postal_code=data.permanent_postal_code,
            ))

        if data.education_level or data.education_institution:
            db.add(EmployeeEducation(
                employee_id=emp.id,
                level=data.education_level or "",
                institution=data.education_institution or "",
                major=data.education_major,
                start_year=data.education_start_year,
                end_year=data.education_end_year,
                graduation_year=data.education_graduation_year,
                certificate_number=data.education_certificate_number,
                graduated=data.education_graduated,
                is_highest=True,
            ))

        if data.bank_id or data.bank_account:
            db.add(EmployeeBank(
                employee_id=emp.id,
                bank_id=data.bank_id,
                account_number=data.bank_account,
                account_holder=data.bank_account_holder,
                is_payroll=True,
                priority=1,
            ))

        if data.emergency_contact_name:
            db.add(EmployeeEmergencyContact(
                employee_id=emp.id,
                name=data.emergency_contact_name,
                phone=data.emergency_contact_phone,
                relation=data.emergency_contact_relationship,
                is_primary=True,
            ))

        if data.contacts:
            for c in data.contacts:
                db.add(EmployeeContact(employee_id=emp.id, **c.model_dump()))

        if data.banks:
            for b in data.banks:
                db.add(EmployeeBank(employee_id=emp.id, **b.model_dump()))

        if data.emergency_contacts:
            for ec in data.emergency_contacts:
                db.add(EmployeeEmergencyContact(employee_id=emp.id, **ec.model_dump()))

        if data.families:
            for f in data.families:
                db.add(EmployeeFamily(employee_id=emp.id, **f.model_dump()))

        db.commit()
        db.refresh(emp)
        return self.get_by_id(db, emp.id)

    def update(self, db: Session, employee_id: int, data: EmployeeUpdate) -> EmployeeResponse:
        emp = employee_core_service.get_by_id(db, employee_id)

        core_updates = {}
        sub_model_updates = {}
        update_fields = data.model_dump(exclude_unset=True)
        core_keys = {
            "employee_number", "full_name", "company_id", "branch_id",
            "department_id", "position_id", "division_id", "job_level_id",
            "employment_status", "employment_type", "join_date",
        }
        for k, v in update_fields.items():
            if k in core_keys:
                core_updates[k] = v
            else:
                sub_model_updates[k] = v

        if core_updates:
            from app.core.organization.employee.schemas import EmployeeUpdate as CoreUpdate
            employee_core_service.update(db, employee_id, CoreUpdate(**core_updates))

        contact_fields = {
            "phone", "alternate_phone", "current_address", "current_province",
            "current_city", "current_district", "current_postal_code",
            "permanent_address", "permanent_province", "permanent_city",
            "permanent_district", "permanent_postal_code",
        }
        edu_fields = {
            "education_level", "education_institution", "education_major",
            "education_start_year", "education_end_year", "education_graduation_year",
            "education_certificate_number", "education_graduated",
        }
        bank_fields = {"bank_id", "bank_account", "bank_account_holder"}
        emergency_fields = {"emergency_contact_name", "emergency_contact_phone", "emergency_contact_relationship"}

        contact_updates = {k: v for k, v in sub_model_updates.items() if k in contact_fields}
        if contact_updates:
            contact = db.query(EmployeeContact).filter(
                EmployeeContact.employee_id == employee_id,
                EmployeeContact.is_primary == True
            ).first()
            if not contact:
                contact = db.query(EmployeeContact).filter(
                    EmployeeContact.employee_id == employee_id
                ).first()
            if not contact:
                contact = EmployeeContact(employee_id=employee_id, contact_type="primary", is_primary=True)
                db.add(contact)
            mapping = {
                "phone": "phone", "alternate_phone": "alternate_phone",
                "current_address": "current_address", "current_province": "current_province",
                "current_city": "current_city", "current_district": "current_district",
                "current_postal_code": "current_postal_code",
                "permanent_address": "permanent_address", "permanent_province": "permanent_province",
                "permanent_city": "permanent_city", "permanent_district": "permanent_district",
                "permanent_postal_code": "permanent_postal_code",
            }
            for req_key, model_attr in mapping.items():
                if req_key in contact_updates:
                    setattr(contact, model_attr, contact_updates[req_key])

        edu_updates = {k: v for k, v in sub_model_updates.items() if k in edu_fields}
        if edu_updates:
            edu = db.query(EmployeeEducation).filter(
                EmployeeEducation.employee_id == employee_id, EmployeeEducation.is_highest == True
            ).first()
            if not edu:
                edu = EmployeeEducation(employee_id=employee_id, is_highest=True)
                db.add(edu)
            mapping = {
                "education_level": "level", "education_institution": "institution",
                "education_major": "major", "education_start_year": "start_year",
                "education_end_year": "end_year", "education_graduation_year": "graduation_year",
                "education_certificate_number": "certificate_number",
                "education_graduated": "graduated",
            }
            for req_key, model_attr in mapping.items():
                if req_key in edu_updates:
                    setattr(edu, model_attr, edu_updates[req_key])

        bank_updates = {k: v for k, v in sub_model_updates.items() if k in bank_fields}
        if bank_updates:
            bank = db.query(EmployeeBank).filter(
                EmployeeBank.employee_id == employee_id, EmployeeBank.is_payroll == True
            ).first()
            if not bank:
                bank = db.query(EmployeeBank).filter(EmployeeBank.employee_id == employee_id).first()
            if not bank:
                bank = EmployeeBank(employee_id=employee_id, is_payroll=True, priority=1)
                db.add(bank)
            if "bank_id" in bank_updates:
                bank.bank_id = bank_updates["bank_id"]
            if "bank_account" in bank_updates:
                bank.account_number = bank_updates["bank_account"]
            if "bank_account_holder" in bank_updates:
                bank.account_holder = bank_updates["bank_account_holder"]

        emergency_updates = {k: v for k, v in sub_model_updates.items() if k in emergency_fields}
        if emergency_updates:
            emergency = db.query(EmployeeEmergencyContact).filter(
                EmployeeEmergencyContact.employee_id == employee_id,
                EmployeeEmergencyContact.is_primary == True
            ).first()
            if not emergency:
                emergency = db.query(EmployeeEmergencyContact).filter(
                    EmployeeEmergencyContact.employee_id == employee_id
                ).first()
            if not emergency:
                emergency = EmployeeEmergencyContact(employee_id=employee_id, is_primary=True)
                db.add(emergency)
            if "emergency_contact_name" in emergency_updates:
                emergency.name = emergency_updates["emergency_contact_name"]
            if "emergency_contact_phone" in emergency_updates:
                emergency.phone = emergency_updates["emergency_contact_phone"]
            if "emergency_contact_relationship" in emergency_updates:
                emergency.relation = emergency_updates["emergency_contact_relationship"]

        db.commit()
        return self.get_by_id(db, employee_id)

    def soft_delete(self, db: Session, employee_id: int, current_user_id: int, reason: Optional[str] = None) -> None:
        emp = employee_core_service.get_by_id(db, employee_id)
        if reason:
            emp.delete_reason = reason
        employee_core_service.soft_delete(db, employee_id, current_user_id)

    def delete(self, db: Session, employee_id: int) -> None:
        employee_core_service.delete(db, employee_id)

    def search(
        self,
        db: Session,
        query_str: str,
        limit: int = 20,
    ) -> List[EmployeeResponse]:
        employees = (
            db.query(Employee)
            .options(
                joinedload(Employee.user),
                joinedload(Employee.company),
                joinedload(Employee.branch),
                joinedload(Employee.department),
                joinedload(Employee.position),
                joinedload(Employee.division),
                joinedload(Employee.job_level),
                joinedload(Employee.contacts),
                joinedload(Employee.educations),
                joinedload(Employee.banks),
                joinedload(Employee.banks).joinedload(EmployeeBank.bank),
                joinedload(Employee.emergency_contacts),
            )
            .join(Employee.user)
            .filter(
                Employee.deleted_at.is_(None),
                Employee.employee_number.ilike(f"%{query_str}%")
                | Employee.full_name.ilike(f"%{query_str}%")
                | User.username.ilike(f"%{query_str}%")
                | User.email.ilike(f"%{query_str}%"),
            )
            .limit(limit)
            .all()
        )
        return [self._build_response(emp) for emp in employees]


employee_service = EmployeeService()
