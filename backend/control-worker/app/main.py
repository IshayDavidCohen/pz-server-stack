from fastapi import FastAPI
from app.api.Routes import router

app = FastAPI(title="Whitelist Worker")
app.include_router(router)
