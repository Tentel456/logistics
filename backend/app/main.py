from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .api.routes import auth, health, oms, transport, warehouse, routing as routing_api, analytics, events

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(transport.router)
app.include_router(warehouse.router)
app.include_router(oms.router)
app.include_router(routing_api.router)
app.include_router(analytics.router)
app.include_router(events.router)

@app.get("/")
async def root():
    return {"service": settings.app_name, "docs": "/docs"}
