from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid


@dataclass
class Event:
    name: str
    data: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    aggregated_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("Event name must not be empty")

    def with_aggregate(self, aggregate_id: str) -> "Event":
        self.aggregated_id = aggregate_id
        return self

    def with_metadata(self, key: str, value: Any) -> "Event":
        self.metadata[key] = value
        return self
