
from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.services.loader import DocumentLoaderService
from app.services.vectorstore import vectorstore

router = APIRouter()

loader = DocumentLoaderService()

UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload_docs")
async def upload_docs(files: list[UploadFile] = File(...)):
    all_docs = []

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load document as LangChain Documents list
        docs = loader.load_file(file_path)

        # Chunk documents
        chunks = loader.chunk_documents(docs)

        all_docs.extend(chunks)

    if not all_docs:
        raise HTTPException(status_code=400, detail="No documents loaded.")

    # Add to vectorstore
    vectorstore.add_documents(all_docs)

    return {
        "message": "Documents uploaded and indexed",
        "chunks_added": len(all_docs)
    }
