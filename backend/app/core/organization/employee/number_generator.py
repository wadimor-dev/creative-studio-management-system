from sqlalchemy.orm import Session
from app.core.organization.employee.models import Employee
from app.core.settings.models import SystemSetting


DEFAULT_FORMAT = "EMP-{YEAR}-{SEQ:05d}"


def _get_format(db: Session) -> str:
    setting = db.query(SystemSetting).filter(
        SystemSetting.key == "employee_number_format"
    ).first()
    if setting and setting.value:
        return setting.value
    return DEFAULT_FORMAT


class EmployeeNumberService:
    def generate(self, db: Session, branch_code: str | None = None, year: int | None = None) -> str:
        if year is None:
            from datetime import date
            year = date.today().year

        fmt = _get_format(db)

        prefix = ""
        suffix = ""
        if "{BRANCH}" in fmt:
            if branch_code:
                fmt = fmt.replace("{BRANCH}", branch_code)
            else:
                fmt = fmt.replace("{BRANCH}-", "")

        last_employee = (
            db.query(Employee)
            .filter(Employee.employee_number.like(f"%-{year}-%"))
            .order_by(Employee.id.desc())
            .first()
        )

        if last_employee and last_employee.employee_number:
            try:
                last_seq = int(last_employee.employee_number.split("-")[-1])
            except (ValueError, IndexError):
                last_seq = 0
        else:
            last_seq = 0

        next_seq = last_seq + 1

        result = fmt.replace("{YEAR}", str(year)).replace("{SEQ}", f"{next_seq:05d}")
        return result


employee_number_service = EmployeeNumberService()
