import os
import shutil
from typing import List, Tuple

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status

from ..app import is_connected
from ..schemas import Product, VisibilityModel

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


def upload_files(path: str, files: List[Tuple[str, File]]):
    os.makedirs(path, exist_ok=True)
    for filename, file in files:
        with open(filename, 'wb') as f:
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
    print(product)
    return await Product.add(product)


@router.get("/{id}/images", response_model=List[str])
async def get_images(id: int):
    product = await Product.get(id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product.photos


@router.post("/{id}/images", response_model=List[str], dependencies=[Depends(is_connected)])
async def upload_images(id: int, tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    for file in files:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail=f"'{file.filename}' is not an image")

    images = await Product.get_photos(id)
    if images is None:
        raise HTTPException(status_code=404, detail="Product not found")

    path = f'/images/products/{id}/'
    filenames = []
    for file in files:
        fn = path + file.filename
        filenames.append(fn)

        if fn in images:
            raise HTTPException(status_code=409, detail=f"The file '{file.filename}' already exists")

        images.append(fn)

    await Product.edit_photos(id, images)

    tasks.add_task(upload_files, path, zip(filenames, (f.file for f in files)))

    return filenames


@router.delete("/{id}/images", response_model=List[str], dependencies=[Depends(is_connected)])
async def delete_images(id: int, files: List[str], tasks: BackgroundTasks):
    path = f'/images/products/{id}/'
    files = [(fn if '/' in fn else path + fn) for fn in files]
    images = await Product.remove_photos(id, files)

    if images is None:
        raise HTTPException(status_code=404, detail="Product not found")

    tasks.add_task(delete_files, files)

    return images

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
