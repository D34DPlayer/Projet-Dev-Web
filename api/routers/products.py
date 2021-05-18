import os
import shutil
from typing import List, Tuple

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status

from ..app import is_connected
from ..schemas import ListProduct, Product, StockModel, VisibilityModel

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


def upload_files(path: str, files: List[Tuple[str, File]]):
    os.makedirs(path, exist_ok=True)
    for filename, file in files:
        with open(filename, "wb") as f:
            shutil.copyfileobj(file, f)


def delete_files(files: List[str]):
    for filename in files:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass


@router.post("", response_model=Product, dependencies=[Depends(is_connected)])
async def add_product(product: Product):
    """Add a product."""
    return await Product.add(product)


@router.get("/{id}/images", response_model=List[str])
async def get_images(id: int):
    product = await Product.get(id)

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product.photos


@router.post("/{id}/images", response_model=List[str], dependencies=[Depends(is_connected)])
async def upload_images(id: int, tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"'{file.filename}' is not an image")

    images = await Product.get_photos(id)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    path = f"/images/products/{id}/"
    filenames = []
    for file in files:
        fn = path + file.filename
        filenames.append(fn)

        if fn in images:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"The file '{file.filename}' already exists"
            )

        images.append(fn)

    await Product.edit_photos(id, images)

    tasks.add_task(upload_files, path, zip(filenames, (f.file for f in files)))

    return filenames


@router.delete("/{id}/images", response_model=List[str], dependencies=[Depends(is_connected)])
async def delete_images(id: int, files: List[str], tasks: BackgroundTasks):
    path = f"/images/products/{id}/"
    files = [(fn if "/" in fn else path + fn) for fn in files]
    images = await Product.remove_photos(id, files)

    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    tasks.add_task(delete_files, files)

    return images


@router.get("", response_model=ListProduct)
async def get_products(page: int = 1, size: int = 50):
    """get a list of product."""
    if page < 1:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Page index must be at least 1.")

    if size > 100:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Page size cannot exceed 100 items.")

    return await Product.get_all(page, size)

@router.get("/{product_id}", response_model=Product)
async def get_product_id(product_id: int):
    """get a product by id"""
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")
    return product


@router.delete("/{product_id}", response_model=Product, dependencies=[Depends(is_connected)])
async def delete_product(product_id: int):
    """Delete an existing product."""
    product = await Product.delete(product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No product with that id was found.")

    return product


@router.put("/{id}/visibility", response_model=Product, dependencies=[Depends(is_connected)])
async def update_product_visibility(id: int, visibility: VisibilityModel):
    """Updates the visibility of a product"""
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The product doesn't exist.")
    if visibility.visibility:
        return await Product.show(id)
    else:
        return await Product.hide(id)


@router.put("/{id}/stock", response_model=Product, dependencies=[Depends(is_connected)])
async def update_stock(id: int, stock: StockModel):
    """Updates the stock of a product"""
    product = await Product.get(id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    return await Product.update(id, stock=stock.stock)


@router.put("/{id}", response_model=Product, dependencies=[Depends(is_connected)])
async def edit_a_product(id: int, product: Product):
    """Updates the information stored about a product."""
    updated_product = await Product.edit(id, product)
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    return updated_product
