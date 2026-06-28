
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.submission import router as submission_router

app = FastAPI(
    title="Ping Submission Agent API",
    description="Automates URL submission across multiple ping services.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(
    submission_router,
    prefix="/api/v1",
    tags=["Submission"],
)


@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Ping Submission Agent",
        "version": "1.0.0",
    }