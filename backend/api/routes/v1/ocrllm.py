import os
import tempfile
from fastapi import APIRouter, UploadFile, HTTPException, Body, Query
from fastapi.params import Form
from pydantic import BaseModel, Field
import asyncio

from schemas.basic import ResponseSuccess
from services.OcrGptService import TesseractOCR_GPT_Service
from core.config import config
import utils.ioutils as ioutils

ocrllm_router = APIRouter(prefix="/ocrllm")


def extract_quote_image(base64_image: str, suffix: str,
                        temperature: float = 0.7, im_preprocess: bool = True,
                        enable_bbox: bool = False):
    """
    Extracts the quote from an image using the OCR service.
    :param base64_image: Base64 encoded image
    :param suffix:  File suffix (e.g. jpg, png, etc.)
    :param temperature:  Temperature for GPT-4 model. Ranges from 0.1 to 1.0.
    :param im_preprocess:  Whether to apply image preprocessing before OCR.
    :return:  OCR results
    """
    # Decode the base64 image string to bytes
    im_bytes = ioutils.base64_decode(base64_image)

    # Initialize the OCR service with specified options
    svc = TesseractOCR_GPT_Service(temperature=temperature, im_preprocess=im_preprocess,
                                   enable_bbox=enable_bbox)

    # Create a temporary file to save the decoded image
    with tempfile.NamedTemporaryFile(suffix=f".{suffix}", dir=config.file.quote_path, delete=False) as temp_file:
        temp_file.write(im_bytes)
        temp_file.seek(0)
        # Run the OCR service on the saved image file
        result = svc.run(temp_file.name)

    # Optionally, save the processed image
    if os.path.exists(temp_file.name):
        svc.save_image(temp_file.name)

    # Return the OCR results
    return result


@ocrllm_router.post("/extract-quote-image/upload/", response_model=ResponseSuccess)
def extract_quote_image_from_file_uploaded(image: UploadFile,
        temperature: float = Form(0.7, description="Temperature for ChatGPT models. Ranges from 0.1 to 1.0."),
        im_preprocess: bool = Form(True, description="Determines whether image preprocessing is applied before OCR."),
        enable_bbox: bool = Form(False, description="Determines whether bounding box output is included in the response.")):
    try:
        suffix = image.filename.split(".")[-1]
        if suffix.lower() not in ["jpg", "jpeg", "png", "gif", "bmp"]:
            raise RuntimeError(f"Unsupported image format: {suffix}. Please upload a valid image file.")
        im_bytes = asyncio.run(image.read())
        base64_image = ioutils.base64_encode(im_bytes)
        result = extract_quote_image(base64_image=base64_image, suffix=suffix,
                                     temperature=temperature, im_preprocess=im_preprocess,
                                     enable_bbox=enable_bbox)
    except (RuntimeError, TypeError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


class OCRLLM_Image(BaseModel):
    base64_image: str  # base64 encoded image data
    format: str = Field(default="JPG",
                        description="Image format (e.g. jpg, png, etc.)")  # image format (e.g. jpg, png, etc.)
    temperature: float = Field(0.7, description="Temperature for GPT-4 model. Ranges from 0.1 to 1.0. Default is 0.7.")
    im_preprocess: bool = Field(True, description="Determines whether image preprocessing is applied before OCR.")
    enable_bbox: bool = Field(False, description="Determines whether bounding box output is included in the response.")


@ocrllm_router.post("/extract-quote-image/base64/", response_model=ResponseSuccess)
def extract_quote_image_from_base64(body: OCRLLM_Image = Body(None, description="")):
    try:
        base64_image = body.base64_image
        suffix = body.format
        im_preprocess = body.im_preprocess
        temperature = body.temperature
        enable_bbox = body.enable_bbox
        result = extract_quote_image(base64_image=base64_image, suffix=suffix,
                                     temperature=temperature, im_preprocess=im_preprocess,
                                     enable_bbox=enable_bbox)
    except (RuntimeError, TypeError) as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result
