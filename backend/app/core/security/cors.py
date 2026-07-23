import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


def _parse_origins() -> list[str]:
    env = os.getenv("CORS_ORIGINS")
    if env:
        import json
        try:
            return json.loads(env)
        except json.JSONDecodeError:
            return [s.strip() for s in env.split(",") if s.strip()]
    return settings.CORS_ORIGINS


def setup_cors(app: FastAPI) -> None:
    origins = _parse_origins()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=r"https?://(.*\.)?idekode\.web\.id",
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=3600,
    )
