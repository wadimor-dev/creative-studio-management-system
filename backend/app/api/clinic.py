"""Thin entrypoint so main.py can import like other routers."""

from app.modules.clinic.router import router

__all__ = ["router"]
