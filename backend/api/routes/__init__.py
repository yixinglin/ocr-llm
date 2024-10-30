from fastapi import APIRouter

from .v1.ocrllm import ocrllm_router
from .v1.imsearch import imsearch_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(ocrllm_router, tags=["OCR-LLM Endpoints"])
v1_router.include_router(imsearch_router, tags=["Image Search Endpoints"])