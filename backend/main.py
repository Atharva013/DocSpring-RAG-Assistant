"""
FastAPI application entrypoint.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import health, sessions, upload

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="DocSpring PDF Chat API",
    description="RAG backend for persistent, session-scoped PDF chat powered by Azure AI services.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten before any public deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(upload.router)
