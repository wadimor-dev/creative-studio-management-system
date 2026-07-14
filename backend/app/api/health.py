from fastapi import APIRouter
from app.common.responses import SuccessResponse, create_success_response

router = APIRouter()

@router.get("/health", response_model=SuccessResponse[dict], tags=["health"])
async def health_check():
    data = {"status": "ok", "app": "Creative Studio Management System"}
    return create_success_response(data=data, message="System is running")
