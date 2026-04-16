from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.routes.routes_machine import router as machine_router

app = FastAPI(title="A3 - Teoria da Computação")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(machine_router)

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"

ASSETS_DIR = FRONTEND_DIR / "assets"

app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

# ===== ELEVADOR =====
@app.get("/style.css")
def get_style():
    return FileResponse(FRONTEND_DIR / "elevator/style.css")


@app.get("/script.js")
def get_script():
    return FileResponse(FRONTEND_DIR / "elevator/script.js")


@app.get("/")
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "elevator/index.html")

# ===== MÁQUINA =====
@app.get("/machine")
def serve_machine():
    return FileResponse(FRONTEND_DIR / "machine/index.html")


@app.get("/machine/style.css")
def get_machine_style():
    return FileResponse(FRONTEND_DIR / "machine/style.css")


@app.get("/machine/script.js")
def get_machine_script():
    return FileResponse(FRONTEND_DIR / "machine/script.js")