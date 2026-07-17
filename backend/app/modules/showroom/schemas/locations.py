from pydantic import BaseModel


class ShowroomLocation(BaseModel):
    id: str
    name: str
