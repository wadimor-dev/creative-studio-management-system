from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum
from app.core.database.base import Base


class DocumentType(str, enum.Enum):
    KTP = "ktp"
    KK = "kk"
    NPWP = "npwp"
    BPJS = "bpjs"
    IJAZAH = "ijazah"
    SERTIFIKAT = "sertifikat"
    KONTRAK = "kontrak"
    SK_MUTASI = "sk_mutasi"
    SK_PROMOSI = "sk_promosi"
    SIM = "sim"
    LAINNYA = "lainnya"


class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False, index=True)
    document_type = Column(String(50), nullable=False)
    document_name = Column(String(200), nullable=True)
    document_number = Column(String(100), nullable=True)
    issue_date = Column(Date, nullable=True)
    expired_at = Column(Date, nullable=True)
    file_path = Column(String(500), nullable=False)
    notes = Column(Text, nullable=True)
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone(timedelta(hours=7))).replace(tzinfo=None))

    employee = relationship("Employee", backref="documents")

    __table_args__ = (
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4"},
    )
