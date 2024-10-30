from typing import List

from models import T_BizProduct


class HsmsVipCRUD:

    async def query_all_products(self) -> List[T_BizProduct]:
        list_products = await T_BizProduct.all()
        return list_products

    async def query_product_by_id(self, product_id: int) -> T_BizProduct:
        product = await T_BizProduct.get(id=product_id)
        return product

    async def query_product_by_article_number(self, article_number: str) -> T_BizProduct:
        product = await T_BizProduct.get(article_number="DBE-1893000")
        return product