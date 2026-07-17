"""Thin entrypoint so main.py can import like other routers."""

from app.modules.showroom.router import router

__all__ = ["router"]
