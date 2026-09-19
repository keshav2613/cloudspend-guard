from fastapi import FastAPI
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.api.routes.resources import router as resources_router
from app.api.routes.dashboard import router as dashboard_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AWS cloud cost visibility and optimization API.",
)

app.include_router(
    health_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    recommendations_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    resources_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    dashboard_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "docs": "/docs",
    }