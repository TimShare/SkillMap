from fastapi import APIRouter, Depends, HTTPException
from src.core.exceptions import NotFoundException, AlreadyExistsException
from src.core.di import get_user_service
from src.interface.schemas.user import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from src.service.user import UserService
from src.service.models import UserDTO
import uuid

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(
    user_data: UserCreateSchema,
    service: UserService = Depends(get_user_service),
):
    try:
        user_dto = UserDTO(
            name=user_data.name,
            email=user_data.email,
            hashed_password=user_data.password,
            is_public=user_data.is_public,
        )
        user_id = await service.create_user(user_dto)
        created_user = await service.get_user(user_id)
        return created_user
    except AlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.get_user(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdateSchema,
    service: UserService = Depends(get_user_service),
):
    try:
        update_dict = user_data.model_dump(exclude_unset=True)
        if "password" in update_dict:
            update_dict["hashed_password"] = update_dict.pop("password")
        
        user_dto = UserDTO(**update_dict)
        updated = await service.update_user(user_id, user_dto)
        return updated
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.delete("/{user_id}", status_code=204)
async def deactivate_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
):
    try:
        await service.deactivate_user(user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)