from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from utils.authentication import get_current_user
from crud.crud_note_model import create_note_db, get_all_users_notes, update_note_db, delete_notes_db
from schemas.notes import NoteSchema
from schemas.user import UserSchema
from typing import Annotated

from environs import env
env.read_env()

router  = APIRouter(
    prefix='/api/users',
    tags=['notes'],
)

@router.get('/{user_id}/notes')
async def get_users(user_id:int, current_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorised access.')
    else:
        user_notes = get_all_users_notes(user_id, db)
        return JSONResponse(content = jsonable_encoder(user_notes),status_code =status.HTTP_200_OK)


@router.post('/{user_id}/notes')
async def create_note(user_id:int,note:NoteSchema,  current_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorised access.')
    else:
        note.user_id = user_id
        try:
            new_note =  create_note_db(note, db)
            return JSONResponse(content = jsonable_encoder(new_note),status_code =status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail =f'{e}')


@router.put('/{user_id}/notes')
async def update_note(user_id:int,note:NoteSchema,  current_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorised access.')
    else:
        try:
            updated_note =  update_note_db(note, db)
            return JSONResponse(content = jsonable_encoder(updated_note),status_code =status.HTTP_202_ACCEPTED)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail =f'{e}')
        
@router.delete('/{user_id}/notes/{note_id}')
async def delete_note(user_id: int, note_id:int,  current_user: Annotated[UserSchema, Depends(get_current_user)], db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Unauthorised access.')
    try:
        deleted_note_msg  = delete_notes_db(note_id, db)
        return JSONResponse(content = jsonable_encoder(deleted_note_msg),status_code =status.HTTP_200_OK)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')
