from fastapi import FastAPI
from app.api.endpoints import model, inference

app = FastAPI(
    title="AI Model Serving Platform",
    description="Backend API for uploading, serving, and monitoring ML models",
    version="0.1.0"
)

# Register routers
app.include_router(model.router, prefix="/api/models", tags=["Models"])
app.include_router(inference.router, prefix="/api/inference", tags=["Inference"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
