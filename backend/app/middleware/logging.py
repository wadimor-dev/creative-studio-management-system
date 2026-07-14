import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        request_id = getattr(request.state, "request_id", "unknown")
        logger.info(f"Request: {request.method} {request.url.path} (ID: {request_id})")
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        logger.info(f"Response: {response.status_code} for {request.url.path} (Time: {process_time:.2f}ms) (ID: {request_id})")
        
        return response
