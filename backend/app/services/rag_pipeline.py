import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from .vectorstore import VectorDBService


class RAGPipeline:
    def __init__(self):
        self.vector_db = VectorDBService()

        # ChatOpenAI requires `openai_api_key`
        self.llm = ChatOpenAI(
            model=os.getenv("DEFAULT_MODEL", "gpt-4.1-mini"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )

        # Output parser
        self.parser = StrOutputParser()

        # Prompt template
        self.prompt = PromptTemplate(
            template="""
You are an AI assistant. Answer the question ONLY using the context below.
If the answer is not in the context, reply exactly:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
""",
            input_variables=["context", "question"]
        )

    def answer_question(self, query: str, top_k: int = 4):
        """RAG flow: retrieve -> prompt -> generate answer"""

        retrieved_docs = self.vector_db.search(query, k=top_k)

        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

        final_prompt = self.prompt.format(
            context=context_text,
            question=query
        )

      
        response = self.llm.invoke(final_prompt)

    
        answer = response.content.strip()

        return {
            "answer": answer,
            "sources": [d.metadata for d in retrieved_docs]
        }
