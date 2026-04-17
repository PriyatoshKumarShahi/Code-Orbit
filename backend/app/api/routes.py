from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.verify import VerifyRequest, VerifyResponse
from app.services.image_service import image_bytes_to_text
from app.services.verifier import verify_content

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "SachAI"}


@router.post("/verify", response_model=VerifyResponse)
async def verify(payload: VerifyRequest) -> VerifyResponse:
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text is required for text verification mode.")
    return await verify_content(payload.text, explain_tone=payload.explain_tone)


@router.post("/verify-image", response_model=VerifyResponse)
async def verify_image(file: UploadFile = File(...)) -> VerifyResponse:
    file_bytes = await file.read()
    extracted = image_bytes_to_text(file_bytes, file.content_type or "image/jpeg")
    return await verify_content(extracted, image_extracted_text=extracted)
