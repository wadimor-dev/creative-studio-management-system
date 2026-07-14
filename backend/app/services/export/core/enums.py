from enum import Enum

class RendererType(str, Enum):
    TABLE = "table"
    BLOCK = "block"
    CARD = "card"
