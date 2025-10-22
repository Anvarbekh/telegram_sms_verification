from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.database import init_db
from app.routers import verification, webhook
from app.config import settings
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Telegram Gateway Verification")
    app.include_router(verification.router)
    app.include_router(webhook.router)

    # Mount static files
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Serve the main UI page
    @app.get("/")
    async def read_root():
        return FileResponse(os.path.join(static_dir, "index.html"))

    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    init_db()


