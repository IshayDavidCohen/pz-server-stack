from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.Routes import router
from app.core.Config import settings

app = FastAPI(title="Whitelist API")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
