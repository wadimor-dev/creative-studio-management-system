import datetime
import random
import string

def _generate_base(prefix: str) -> str:
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    # Generates a random 5 digit string. In a real system, this would be tied to a sequence in DB.
    # For now, it satisfies the required format XXX-YYYYMMDD-00001
    seq = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}-{date_str}-{seq}"

def generate_item_code() -> str:
    return _generate_base("ITM")

def generate_report_code() -> str:
    return _generate_base("RPT")

def generate_reference() -> str:
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    seq = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"REF-{date_str}-{seq}"


def generate_work_reference(activity_id: int) -> str:
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    return f"ACT-{date_str}-{activity_id:05d}"
