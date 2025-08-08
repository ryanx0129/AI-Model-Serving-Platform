#-------------------------------From Phase 1------------------------------------
#-- Placeholder for all model upload, versioning, and listing logic.          --
#-- What it does so far = Just returns a placeholder response for /api/models --
#-------------------------------------------------------------------------------

# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/")
# def list_models():
#     return {"message": "List of available models will be shown here."}

#-------------------------------From Phase 2------------------------------------
#-- Placeholder for all model upload, versioning, and listing logic.          --
#--                                                                           --
#-- What it does right now :                                                  --
#--    Accepts a model file (UploadFile)                                      --
#--    Accepts form fields: 'model_name', 'version', 'model_type'.            --
#--    Saves the file locally into /uploaded_models                           --
#--    Returns a success response with metadata                               --
#-------------------------------------------------------------------------------

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from datetime import datetime
from pathlib import Path
import shutil

from app.models.schema import ModelMetadata

router = APIRouter()

# Directory to store uploaded model files
UPLOAD_DIR = Path("uploaded_models")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory model registry (we'll replace with DB later)
model_registry = {}

@router.post("/upload")
async def upload_model(
    file: UploadFile = File(...),
    model_name: str = Form(...),
    version: str = Form(...),
    model_type: str = Form(...)  # e.g., "nlp", "vision"
):
    try:
        model_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        filename = f"{model_name}_{version}_{model_id}{Path(file.filename).suffix}"
        file_path = UPLOAD_DIR / filename

        # Save the model file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Register metadata in memory
        metadata = ModelMetadata(
            model_id=model_id,
            name=model_name,
            version=version,
            model_type=model_type,
            file_path=str(file_path),
            uploaded_at=timestamp
        )
        model_registry[model_id] = metadata

        return JSONResponse(content={"message": "Model uploaded successfully", "model_id": model_id}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/")
def list_models():
    return {"models": [m.dict() for m in model_registry.values()]}
