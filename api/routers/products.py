from fastapi import APIRouter, Depends, status, HTTPException

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


@router.get("", response_model=list[Product])
async def get_products():
    """get a list of product."""
    return await Product.get_all()


@router.delete("/{product_id}", response_model=Product, dependencies=[Depends(is_connected)])
async def delete_product(product_id: int):
    """Delete an existing product."""
    product = await Product.delete(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")

    return product
