"""FastAPI application and direct launcher for hardware mode."""

import time
import webbrowser
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from .database import initialize_database
from .realtime.websocket_manager import active_connections, broadcast
from .routes import calibration, gameplay, pages
from .settings import PROJECT_ROOT

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database at startup and close WebSockets at shutdown."""
    initialize_database()
    yield
    if active_connections:
        await broadcast("The server is shutting down. Disconnecting...")
        active_connections.clear()


app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=str(PROJECT_ROOT / "singonlight" / "static")),
    name="static",
)
pages.register_routes(app)
calibration.register_routes(app)
gameplay.register_routes(app)


if __name__ == "__main__":
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8001")
    uvicorn.run(
        "singonlight.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        reload_dirs=[str(PROJECT_ROOT / "singonlight")],
    )
