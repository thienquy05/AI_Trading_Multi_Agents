from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth

app = FastAPI(title="AI Trading Multi-Agents API")

# Pinned to the single frontend origin — no wildcard, ever: these
# endpoints will eventually guard capital (scaffold-roadmap §2).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_settings().frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": get_settings().environment}
