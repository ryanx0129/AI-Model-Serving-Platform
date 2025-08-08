#Phase 2: This lets FastAPI validate and serialize the metadata cleanly.
from pydantic import BaseModel

class ModelMetadata(BaseModel):
    model_id: str
    name: str
    version: str
    model_type: str
    file_path: str
    uploaded_at: str
