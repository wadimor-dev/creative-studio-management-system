import re

def is_positive(value: int) -> bool:
    return value > 0

def is_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_phone(phone: str) -> bool:
    pattern = r"^\+?[1-9]\d{1,14}$"
    return re.match(pattern, phone) is not None

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    # Basic sanitize
    return text.strip()

def is_empty(text: str) -> bool:
    return not text or not text.strip()

def max_length(text: str, maximum: int) -> bool:
    if not text:
        return True
    return len(text) <= maximum
