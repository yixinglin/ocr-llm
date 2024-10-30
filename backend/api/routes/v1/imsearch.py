import asyncio
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, UploadFile, HTTPException

from schemas.basic import ResponseSuccess
from services.hsms_vip import VipProductSearchService

imsearch_router = APIRouter(prefix="/imsearch")

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


