from fastapi import APIRouter, Depends, HTTPException, status

from typing import List

from ..app import is_connected, get_password_hash

from ..schemas import User, DBUser, CreateUser


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(is_connected)],
)


@router.get("/me", response_model=User)
async def get_current_user(user: User = Depends(is_connected)):
    """Provides information about the user logged in."""
    return user


@router.get("/{username}", response_model=User)
async def get_some_user(username: str):
    """Provides information about an user."""
    user = await DBUser.get(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user


@router.put("/{username}", response_model=User)
async def update_some_user(username: str, user: CreateUser):
    """Updates the information stored about an user. Password included."""
    hashed_pwd = get_password_hash(user.password)

    updated_user = DBUser(**user.dict(), hashed_password=hashed_pwd)

    updated_user = await DBUser.update(username, updated_user)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return updated_user


@router.delete("/{username}", response_model=User)
async def delete_some_user(username: str, user: User = Depends(is_connected)):
    """Deletes an existing user."""
    if user.username == username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't delete your own user.")

    user = await DBUser.delete(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")

    return user


@router.post("", response_model=User)
async def create_a_new_user(user: CreateUser):
    """Creates a new user."""
    old_user = await DBUser.get(user.username)
    if old_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The username is already in use.")

    hashed_pwd = get_password_hash(user.password)

    new_user = DBUser(**user.dict(), hashed_password=hashed_pwd)

    new_user = await DBUser.create(new_user)

    if not new_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The user couldn't be created.")

    return new_user


@router.get("", response_model=List[User])
async def get_all_the_users():
    """Provides information about all the users stored."""
    users = await DBUser.get_all()

    return users
