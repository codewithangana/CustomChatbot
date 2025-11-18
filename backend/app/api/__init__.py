from fastapi import APIRouter

from .ask import router as ask_router
from .uploadDocs import router as upload_docs_router
from .deleteDocs import router as delete_docs_router   

api_router = APIRouter()

# include all API endpoints here
api_router.include_router(ask_router, prefix="/rag", tags=["Ask"])
api_router.include_router(upload_docs_router, prefix="/documents", tags=["Upload"])
api_router.include_router(delete_docs_router, prefix="/documents", tags=["Delete"])

__all__ = ["api_router"]
