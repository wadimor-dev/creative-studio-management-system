from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Initialize resources here
    yield
    logger.info("Application shutting down...")
    # Clean up resources here
