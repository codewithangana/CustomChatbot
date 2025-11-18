import os
from typing import List

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentLoaderService:
    def __init__(self, chunk_size=800, chunk_overlap=200):
        """Initialize text splitter for chunking."""
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_text(self, text: str) -> List[Document]:
        """Load raw text directly into a LangChain Document."""
        return [Document(page_content=text)]

    def load_file(self, file_path: str) -> List[Document]:
        """Load a file (.txt, .pdf, .docx) into LangChain Documents."""
        ext = os.path.splitext(file_path)[-1].lower()

        if ext == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
            return loader.load()

        elif ext == ".pdf":
            loader = PyPDFLoader(file_path)
            return loader.load()

        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
            return loader.load()

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def chunk_documents(self, docs: List[Document]) -> List[Document]:
        """Split documents into smaller chunks."""
        return self.splitter.split_documents(docs)
