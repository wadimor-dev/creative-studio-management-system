from fastapi import status
from app.core.exceptions import AppException

class ReportException(AppException):
    pass

class ReportNotFoundException(ReportException):
    def __init__(self, message="Report not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class InvalidReportPeriodException(ReportException):
    def __init__(self, message="Invalid report period"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)
