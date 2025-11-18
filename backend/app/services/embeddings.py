from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from app.core.config import settings   

class EmbeddingService:
    def __init__(self):
        api_key = settings.OPENAI_API_KEY   

        self.model = OpenAIEmbeddings(
            api_key=api_key,
            model="text-embedding-3-small"
        )

    def embed_documents(self, docs: list[Document]):
        texts = [d.page_content for d in docs]
        return self.model.embed_documents(texts)

    def embed_query(self, query: str):
        return self.model.embed_query(query)
