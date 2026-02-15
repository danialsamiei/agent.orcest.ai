# Entry point for Render/uvicorn: uvicorn main:app
# Re-exports the FastAPI app from openhands.server.app
from openhands.server.app import app

__all__ = ["app"]
