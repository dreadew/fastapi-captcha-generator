from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user, _delete_user, _get_me, _get_user_by_id, _update_user
from api.schemas import DeleteUserResponse, ShowCaptcha, ShowUser, UpdateUserRequest, UpdatedUserResponse, UserCreate, UserFind

from db.session import get_db
from utils.captcha import gen_captcha_img

user_router = APIRouter()

@user_router.post('/', response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
	return await _create_new_user(body, db)

@user_router.delete('/', response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user 

@user_router.get("/me", response_model=ShowUser)
async def get_me(
    body: UserFind,
    db: AsyncSession = Depends(get_db)
) -> ShowUser:
    user = await _get_me(body.access_token, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail="Error user with this access_token not found"
        )
    return user 

@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db)
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


utils_router = APIRouter()
@utils_router.get('/captcha')
async def generate_captcha() -> ShowCaptcha:
	captcha_image, captcha_data, icons = await gen_captcha_img()
	return JSONResponse(content={'img': captcha_image, 'data': captcha_data, 'icons': icons})