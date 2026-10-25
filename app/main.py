from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
        version=settings.app_version,
            description="Varul backend foundation service.",
            )

app.include_router(health_router, prefix=settings.api_prefix)


@app.get("/")
async def root() -> dict[str, str]:
                return {
                        "service": settings.app_name,
                        "status": "ok",
                        "version": settings.app_version,
                }