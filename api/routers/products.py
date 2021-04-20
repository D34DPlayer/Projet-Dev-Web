from fastapi import APIRouter, Depends, HTTPException, status

from ..app import is_connected

from ..schemas import Product, VisibilityModel


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

@router.put("/{id}/visibility", response_model=Product, dependencies=[Depends(is_connected)])
async def update_product_visibility(id: int, visibility: VisibilityModel):
    """Updates the visibility of a product"""
    product = await Product.get(id)
    if not product:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="The product doesn't exist.")
    if visibility.visibility:
        return await Product.show(id)
    else:
        return await Product.hide(id)
