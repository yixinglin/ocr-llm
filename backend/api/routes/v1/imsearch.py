import asyncio
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, UploadFile, HTTPException, Body
from pydantic import Field, BaseModel

from schemas.basic import ResponseSuccess
from services.hsms_vip import VipProductSearchService
from utils import ioutils

imsearch_router = APIRouter(prefix="/imsearch")

class Base64Image(BaseModel):
    base64_image: str  # base64 encoded image data
    format: str = Field(default="JPG",
                        description="Image format (e.g. jpg, png, etc.)")  # image format (e.g. jpg, png, etc.)


def search_images_by_image(image: bytes, k):
    pil_image = Image.open(BytesIO(image))
    pil_image = pil_image.convert("RGB")
    svc = VipProductSearchService()
    df, image_url_list = svc.search_products_by_image(pil_image, k=k)
    df["image_url"] = image_url_list
    product_list = df.to_dict(orient="records")
    data = {"products": product_list, "total": len(product_list)}
    return ResponseSuccess(data=data)

@imsearch_router.post("/upload/")
def search_images_by_upload(image: UploadFile):
    try:
        im_data = asyncio.run(image.read())
        result = search_images_by_image(im_data, k=8)
        return result
    except (RuntimeError, TypeError) as e:
        raise HTTPException(status_code=500, detail=str(e))

@imsearch_router.post("/base64/")
def search_images_by_base64(body: Base64Image = Body(None, description="Base64 encoded image data")):
    try:
        im_data = ioutils.base64_decode(body.base64_image)
        result = search_images_by_image(im_data, k=8)
        return result
    except (RuntimeError, TypeError) as e:
        raise HTTPException(status_code=500, detail=str(e))
