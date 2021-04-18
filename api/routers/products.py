from fastapi import APIRouter, Depends

from ..app import is_connected

from ..schemas import Product


router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post("", response_model=Product, dependencies=[Depends(is_connected)])
async def add_product(product: Product):
    """Add a product."""
    print(product)
    return await Product.add(product)
