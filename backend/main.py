from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controllers import router as api_router
from database import init_db
import os

app = FastAPI(title="Excalibur C2", version="1.0")

# CORS (allow all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Serve frontend
panel_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../panel"))
app.mount("/", StaticFiles(directory=panel_dir, html=True), name="panel")

@app.on_event("startup")
async def startup_event():
    init_db()

# Run with: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
