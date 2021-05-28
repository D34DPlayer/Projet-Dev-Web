import dataclasses as dc
import os
import shutil
from typing import List, Tuple

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from ..app import is_connected
from ..schemas import ListProduct, PageModel, Product, StockModel, VisibilityModel

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


def filter(model: BaseModel):
    def get_fields(self) -> dict:
        """Validate then return the fields."""
        fields = {}

        for key, value in dc.asdict(self).items():
            if value is not None:
                # Check the length to be at least 3 characters.
                if isinstance(value, str) and len(value) < 3:
                    raise ValueError(f'The field {key!r} must have at least 3 characters.')

                fields[key] = value

        return fields

    # Extract the fields from the model
    fields = [(name, field.type_, dc.field(default=None)) for name, field in model.__fields__.items()]
    # and create a dataclass from these fields.
    return dc.make_dataclass(f'Filter[{model.__name__}]', fields, namespace=dict(dict=get_fields))


def upload_files(path: str, files: List[Tuple[str, File]]):
    """Upload files to disk."""
    # Make sure the folder exists
    os.makedirs(path, exist_ok=True)
    for filename, file in files:
        with open(filename, "wb") as f:
            # copy the file to the disk
            shutil.copyfileobj(file, f)


def delete_files(files: List[str]):
    """Delete files on the disk."""
    for filename in files:
        try:
            # Try to remove it
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
async def get_products(page: PageModel = Depends(PageModel)):
    """get a list of product."""
    return await Product.get_all(page)


@router.get("/search", response_model=ListProduct)
async def search_products(fields=Depends(filter(Product)), page: PageModel = Depends(PageModel)):
    """search a list of matching products."""
    try:
        return await Product.find(page, **fields.dict())
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


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
