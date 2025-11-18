from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.ask import router as ask_router
from app.api.uploadDocs import router as upload_router
from app.api.deleteDocs import router as delete_router
from app.api.token import router as token_router




app = FastAPI(
    title="Custom Chatbot",
    version="1.0"
)

# CORS (Allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(ask_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(delete_router, prefix="/api")
app.include_router(token_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "RAG Chatbot Backend Running"}
