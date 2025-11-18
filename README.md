# custom RAG Chatbot (FastAPI + LangChain + ChromaDB)

This project is a **custom Retrieval-Augmented Generation (RAG) chatbot** built using:

- **FastAPI** (backend API)
- **LangChain** embeddings + text splitting
- **ChromaDB** (Vectorstore)
- **OpenAI / LLaMA / Any embedding model**
- **Document upload + delete + search**
- **Fully persistent vector index**

---

## Features

- Upload PDFs, DOCX, TXT files
- Auto-chunk + embed documents
- Persistent Chroma vector store saved in `./vectorstore/index`
- Delete documents from vector DB
- Query the RAG pipeline using `/api/ask`
- OpenAI compatible chat response

---

## Project Structure

