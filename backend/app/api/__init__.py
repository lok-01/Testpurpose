from app.api.routes_profile import router as profile_router
from app.api.routes_chart import router as chart_router
from app.api.routes_calculations import router as calculations_router
from app.api.routes_ai import router as ai_router
from app.api.routes_verification import router as verification_router
from app.api.routes_settings import router as settings_router

__all__ = [
    "profile_router",
    "chart_router",
    "calculations_router",
    "ai_router",
    "verification_router",
    "settings_router",
]
