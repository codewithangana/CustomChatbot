import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from .embeddings import EmbeddingService


class VectorDBService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.db_path = os.getenv("CHROMA_DIR", "./vectorstore/index")

        # Initialize persistent Chroma DB (auto-persists)
        self.db = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embedding_service.model
        )

    def add_documents(self, docs: list[Document]):
        """Add documents and automatically persist."""
        self.db.add_documents(docs)
       

    def search(self, query: str, k: int = 5):
        """Retrieve top-K relevant documents."""
        return self.db.similarity_search(query, k=k)

    def delete_all(self):
        """Delete the entire vector store and recreate."""
        import shutil

        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

        os.makedirs(self.db_path, exist_ok=True)

        # Reinitialize empty database
        self.db = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embedding_service.model
        )


# Global shared instance
vectorstore = VectorDBService()
