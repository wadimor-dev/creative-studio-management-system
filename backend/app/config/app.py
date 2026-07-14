from pydantic import BaseModel

class AppConfig(BaseModel):
    name: str = "Creative Studio Management System"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    description: str = "Core backend system"

app_config = AppConfig()
