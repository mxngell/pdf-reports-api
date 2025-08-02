from fastapi import FastAPI
from exceptions.handlers import register_exception_handlers
from logger import log
from router import router
from config import settings
import uvicorn

app = FastAPI(
    title="PDF reports API",
    redoc_url=None,
    version="1.0.0"
)

register_exception_handlers(app)

app.include_router(router)

if __name__ == "__main__":
    log.info("API started")
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
    log.info("API stopped")