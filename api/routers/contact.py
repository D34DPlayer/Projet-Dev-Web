import re

from fastapi import APIRouter, Depends, HTTPException, status

from ..app import is_connected
from ..schemas import Contact

REGEX_PHONE = re.compile(r"[0-9 ]+")
REGEX_EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
REGEX_FACEBOOK = re.compile(r"https?://(www\.)?facebook\.com/.+")


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
    invalid = []

    # Validate inputs
    if not REGEX_PHONE.match(contact.phone.mobile):
        invalid.append(("contact.phone.mobile", contact.phone.mobile))

    if not REGEX_PHONE.match(contact.phone.office):
        invalid.append(("contact.phone.office", contact.phone.office))

    if not REGEX_EMAIL.match(contact.email):
        invalid.append(("contact.email", contact.email))

    if not REGEX_FACEBOOK.match(contact.facebook):
        invalid.append(("contact.facebook", contact.facebook))

    if len(invalid) > 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"fields": [f"{value!r} is not a valid value for {field}" for field, value in invalid]},
        )

    return await Contact.edit(contact)
