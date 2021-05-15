from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from ..app import is_connected

from ..schemas import MessageBrief, Message, SeenModel


router = APIRouter(
    prefix="/contact",
    tags=["messages"],
)


@router.get("", response_model=List[MessageBrief], dependencies=[Depends(is_connected)])
async def get_all_the_comments():
    """Get a small description for all the comments."""
    messages = await Message.get_all()
    return messages


@router.post("", response_model=Message)
async def send_a_comment(message: Message):
    """Provides information about an user."""
    message = await Message.add(message)
    if not message:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The message couldn't be sent.")

    return message


@router.put("/{id}", response_model=Message, dependencies=[Depends(is_connected)])
async def get_a_comment(id: int):
    """Provides all the info about a specific comment."""

    message = await Message.get(id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found.")

    return message


@router.delete("/{id}", response_model=Message, dependencies=[Depends(is_connected)])
async def delete_a_comment(id: int):
    """Deletes a comment from the database."""

    message = await Message.delete(id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found.")

    return message


@router.put("/{id}/seen", response_model=Message, dependencies=[Depends(is_connected)])
async def see_a_comment(id: int, body: SeenModel):
    """Changes if a comment is marked as seem or not."""

    message = await Message.change_seen(id, body.seen)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found.")

    return message
