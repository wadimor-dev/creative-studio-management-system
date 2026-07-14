from enum import Enum

class WorkActivityStatus(str, Enum):
    READY = "READY"
    WORKING = "WORKING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WorkEvidenceType(str, Enum):
    BEFORE = "BEFORE"
    PROGRESS = "PROGRESS"
    AFTER = "AFTER"
