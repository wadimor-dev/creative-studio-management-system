"""Thin entrypoint so main.py can import like other routers."""

from app.modules.hrd_ga.clinic.router import router

__all__ = ["router"]
