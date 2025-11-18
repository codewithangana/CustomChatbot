from fastapi import APIRouter, HTTPException
import os
import shutil

from app.core.logger import logger
from app.services.vectorstore import VectorDBService  
from app.core.config import settings

router = APIRouter()

DATA_FOLDER = "data"
VECTORSTORE_FOLDER = "vectorstore"


@router.delete("/delete-docs")
def delete_documents(doc_names: list[str] | None = None):
    """
    Delete documents from /data.
    If doc_names=None → delete ALL documents.
    After deleting, rebuild vectorstore.
    """

    # Case 1: Delete ALL documents
    if doc_names is None:
        logger.info("Deleting ALL documents...")

        # Delete everything inside /data
        if os.path.exists(DATA_FOLDER):
            for f in os.listdir(DATA_FOLDER):
                file_path = os.path.join(DATA_FOLDER, f)
                os.remove(file_path)

        # Delete the entire vectorstore folder
        if os.path.exists(VECTORSTORE_FOLDER):
            shutil.rmtree(VECTORSTORE_FOLDER)

        # Recreate empty vectorstore folder
        os.makedirs(VECTORSTORE_FOLDER, exist_ok=True)

        logger.info("All documents + vectorstore cleared.")
        return {"message": "All documents deleted and vectorstore cleared."}

    # Case 2: Delete specific documents
    deleted = []
    not_found = []

    for doc in doc_names:
        path = os.path.join(DATA_FOLDER, doc)

        if os.path.exists(path):
            os.remove(path)
            deleted.append(doc)
            logger.info(f"Deleted: {doc}")
        else:
            not_found.append(doc)
            logger.warning(f"File not found: {doc}")

    # Rebuild the vectorstore
    try:
        logger.info("Rebuilding vectorstore after deletion...")
        vector_service = VectorDBService()      
        vector_service.delete_all()             
        logger.info("Vectorstore rebuilt successfully.")
    except Exception as e:
        logger.error(f"Error rebuilding vectorstore: {e}")
        raise HTTPException(500, detail="Vectorstore rebuild failed")

    return {
        "deleted": deleted,
        "not_found": not_found,
        "message": "Deletion completed and vectorstore rebuilt."
    }
