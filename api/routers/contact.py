from fastapi import APIRouter, Depends

from ..app import is_connected
from ..schemas import Contact

router = APIRouter(
    prefix="/contact",
    tags=["contact"],
)

@router.get("", response_model=Contact)
async def get_contact():
    """Get contact informations."""
    return await Contact.get()

@router.put("", response_model=Contact, dependencies=[Depends(is_connected)])
async def edit_contact(contact: Contact):
    """Modify contact informations."""
    return await Contact.edit(contact)
