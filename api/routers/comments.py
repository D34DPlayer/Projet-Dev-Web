from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from ..app import is_connected

from ..schemas import CommentBrief, Comment, SeenModel

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.get("", response_model=List[CommentBrief], dependencies=[Depends(is_connected)])
async def get_all_the_comments():
    """Get a small description for all the comments."""
    comments = await Comment.get_all()
    return comments


@router.post("", response_model=Comment)
async def send_a_comment(comment: Comment):
    """Provides information about an user."""
    comment = await Comment.add(comment)
    if not comment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The comment couldn't be sent.")

    return comment


@router.get("/{id}", response_model=Comment, dependencies=[Depends(is_connected)])
async def get_a_comment(id: int):
    """Provides all the info about a specific comment."""

    comment = await Comment.get(id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")

    return comment


@router.delete("/{id}", response_model=Comment, dependencies=[Depends(is_connected)])
async def delete_a_comment(id: int):
    """Deletes a comment from the database."""

    comment = await Comment.delete(id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")

    return comment


@router.put("/{id}/seen", response_model=Comment, dependencies=[Depends(is_connected)])
async def see_a_comment(id: int, body: SeenModel):
    """Changes if a comment is marked as seem or not."""

    comment = await Comment.change_seen(id, body.seen)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")

    return comment


@router.put("/seen", response_model=list[Comment], dependencies=[Depends(is_connected)])
async def see_list_comment(body: SeenModel):
    if body.comments is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="List Id is required.")
    comment = await Comment.change_list_seen(body.comments, body.seen)

    return comment
