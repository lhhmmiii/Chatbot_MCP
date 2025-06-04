from fastapi import APIRouter
from utils import create_metadata
from schemas import DocumentMetadata


metadata_router = APIRouter(prefix="/metadata", tags=["metadata"])

@metadata_router.post("/create_metadata", response_model=DocumentMetadata)
def create_metadata_endpoint(text: str, file_name: str, label: str) -> DocumentMetadata:
    metadata = create_metadata(text, file_name, label)
    return DocumentMetadata(**metadata)


