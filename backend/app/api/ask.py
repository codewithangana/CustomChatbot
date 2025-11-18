# app/api/ask.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

from app.core.cache import cache               
from app.core.openai_client import openai_client 
from app.core.security import verify_token     
from app.services.rag_pipeline import RAGPipeline  

router = APIRouter()
logger = logging.getLogger(__name__)


pipeline = RAGPipeline()


class AskRequest(BaseModel):
    question: str
    top_k: Optional[int] = 4  


@router.post("/ask")
async def ask_question(
    payload: AskRequest,
    token: dict = Depends(verify_token)   
):
    """
    Ask endpoint:
    - Checks Redis cache first
    - Uses RAG pipeline to retrieve and generate answer if cache miss
    - Caches the final answer
    """

    question = (payload.question or "").strip()
    k = payload.top_k or 4

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    
    cache_key = f"answer:{question.strip().lower()}"


    try:
        cached = cache.get(cache_key)
        if cached:
            logger.info("Cache hit for question")
            
            return {
                "answer": cached,
                "sources": [],     
                "cached": True
            }
    except Exception as e:
        # Cache errors should not block the request; log and continue
        logger.warning(f"Redis cache access error: {e}")

    # 2) Retrieve & generate using RAG pipeline
    try:
       
        result = pipeline.answer_question(query=question, top_k=k)

        answer = result.get("answer", "").strip()
        sources = result.get("sources", [])
    except Exception as e:
        logger.error(f"RAG pipeline error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Retrieval/Generation error: {str(e)}")

    # If there's no answer or it's empty, respond accordingly
    if not answer:
        answer = "I don't know based on the provided documents."

    
    try:
        # set TTL in seconds (e.g., 1 hour). adjust as needed.
        cache.set(cache_key, answer, ex=3600)
    except Exception as e:
        logger.warning(f"Failed to write to cache: {e}")


    return {
        "answer": answer,
        "sources": sources,
        "cached": False
    }
