from fastapi import APIRouter, Depends, HTTPException

from ..app import is_connected, get_password_hash

from ..schemas import User, DBUser, CreateUser


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(is_connected)],
)


@router.get("/me", response_model=User)
async def get_current_user(user: User = Depends(is_connected)):
    return user


@router.get("/{username}", response_model=User)
async def get_some_user(username: str):
    user = await DBUser.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.put("/{username}", response_model=User)
async def update_some_user(username: str, user: CreateUser):
    if user.username != username:
        raise HTTPException(status_code=400, detail="You can't change the user's username.")

    hashed_pwd = get_password_hash(user.password)

    updated_user = DBUser(**user.dict(), hashed_password=hashed_pwd)

    updated_user = await DBUser.update(updated_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return updated_user


@router.delete("/{username}", response_model=User)
async def delete_some_user(username: str, user: User = Depends(is_connected)):
    if user.username == username:
        raise HTTPException(status_code=400, detail="You can't delete your own user.")

    user = await DBUser.delete(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


@router.post("/", response_model=User)
async def create_a_new_user(user: CreateUser):
    old_user = await DBUser.get(user.username)
    if old_user:
        raise HTTPException(status_code=400, detail="The username is already in use.")

    hashed_pwd = get_password_hash(user.password)

    new_user = DBUser(**user.dict(), hashed_password=hashed_pwd)

    new_user = await DBUser.create(new_user)

    if not new_user:
        raise HTTPException(status_code=501, detail="The user couldn't be created.")

    return new_user
