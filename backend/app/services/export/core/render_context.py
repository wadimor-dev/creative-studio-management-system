from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RenderContext:
    orientation: str = "P" # P for Portrait, L for Landscape
    page_size: str = "A4"
    margin: int = 15
    company_logo: Optional[str] = None
    theme: str = "default"
    metadata: dict = field(default_factory=dict)
