# Entry point for Render/uvicorn: uvicorn main:app
# Uses listen.py which mounts frontend at / and includes SocketIO
# Requires frontend/build from: cd frontend && npm run build
from openhands.server.listen import app

__all__ = ["app"]
