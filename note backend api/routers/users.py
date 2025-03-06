from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from utils.authentication import  authenticate_user, generate_login_token, get_current_user
from crud.crud_user_model import create_user_db, update_user_db, delete_user_db
from schemas.user import UserSignUpSchema, UserSchema, UserLoginSchema
from typing import Annotated


from environs import env
env.read_env()

router  = APIRouter(
    prefix='/api/users',
    tags=['users'],
)

@router.get('/')
async def get_users(current_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.role_id == int(env('USER_ADMIN_ID')):
        return 
    else:
        return current_user

@router.post('/token')
async def login_user( form_data: Annotated[OAuth2PasswordRequestForm, Depends()],):
    #Remember to check that the user email is verified and the user.deleted is false
    user = UserLoginSchema(email = form_data.username, password= form_data.password)
    user_authenticated = authenticate_user(user)
    if not user_authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return generate_login_token(user_authenticated.email)

@router.post('/')
async def create_user(user: UserSignUpSchema, db: Session = Depends(get_db)):
    '''
    This function create a new user.
    '''
    try:
        new_user = create_user_db(user,db)
        return JSONResponse(content = jsonable_encoder(new_user),status_code =status.HTTP_201_CREATED)
    except  ValueError as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f'{e}')
    
    
@router.put('/')
async def update_user(user: UserSignUpSchema, curent_user: Annotated[UserSchema, Depends(get_current_user)],  db: Session = Depends(get_db)):
    '''This function update the user record.'''
    if curent_user.id != user.id or curent_user.role_id !=  int(env('USER_ADMIN_ID')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unable to delete user.')
    try:
        existing_user  = update_user_db(user, db)
        return JSONResponse(content = jsonable_encoder(existing_user),status_code =status.HTTP_200_OK)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

@router.delete('/{user_id}')
async def delete_user(user_id: int, curent_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    '''This function delete a user, like deactivate the user.'''
    if curent_user.id != user_id or curent_user.role_id !=  int(env('USER_ADMIN_ID')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'You cannot delete user.')
    try:
        deleted_user_msg  = delete_user_db(user_id, db)
        return JSONResponse(content = jsonable_encoder(deleted_user_msg),status_code =status.HTTP_200_OK)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')

