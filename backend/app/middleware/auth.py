from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from jose import jwt, JWTError
import logging
import time

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Trace Request
        start_time = time.time()
        
        # Inject default user state
        request.state.user = None
        
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Basic decode without DB verification
                # We need SECRET_KEY and ALGORITHM but since this is just middleware 
                # we can rely on dependencies for strict validation, 
                # but middleware injects the basic info.
                from app.core.config import settings
                from app.core.jwt import ALGORITHM
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
                
                request.state.user = {
                    "sub": payload.get("sub"),
                    "role": payload.get("role")
                }
            except JWTError:
                pass
                
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.debug(f"Request: {request.method} {request.url.path} - Time: {process_time:.4f}s")
        
        return response
