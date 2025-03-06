from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import select
from models.note import NoteModel
from schemas.notes import NoteSchema
from datetime import datetime

from environs import env
env.read_env()

def get_note_by_field(model_field:InstrumentedAttribute, value:str, db:Session, is_single_record =False):
    ''' Get notes record by a field name(such as note_tile, user_id, note_id) specified as parameter.'''
    if is_single_record:
        return db.scalars(select(NoteModel).where( model_field == value)).first()
    return db.scalars(select(NoteModel).where( model_field == value and NoteModel.deleted_status == False )).all()

def get_all_users_notes(user_id:int, db:Session):
    ''' Get all user's notes.'''
    #return db.scalars(select(NoteModel).where( NoteModel.user_id == user_id)).all()
    return get_note_by_field(NoteModel.user_id,  user_id, db, is_single_record=False)


def create_note_db(note: NoteSchema, db:Session):
    ''' Function to create a notes.'''
    existing_note = get_note_by_field(NoteModel.note_title, note.note_title, db, is_single_record=True)
    if existing_note:
        raise ValueError(f'Note with title{note.note_title} already exists. Note title should be unique.')
    new_note = NoteModel()
    for field in ['note_title', 'note_content', 'public_status', 'user_id', 'public_status']:
            setattr(new_note, field, getattr(note,field))
    
    with db as db_session:
        db_session.add(new_note)
        db_session.commit()
        db_session.refresh(new_note)
    return NoteSchema(**new_note.__dict__)

def update_note_db(note:NoteSchema, db:Session):
    '''This function update a note'''
    existing_note  = get_note_by_field(NoteModel.note_id, note.note_id, db, is_single_record=True )
    existing_note.date_updated = datetime.now()
    if  existing_note:
        existing_note.date_updated = datetime.now()
        for field in ['note_title', 'note_content', 'public_status', 'deleted_status', 'user_id', 'public_status']:
            setattr(existing_note, field, getattr(note,field))
        db.commit()
        db.refresh(existing_note)
        return existing_note
    else:
        raise ValueError(f'User with id {note.note_id.id} does not exist.')
    
def delete_notes_db(note_id: int, db: Session):
    note_to_delete =  get_note_by_field(NoteModel.note_id,note_id, db, is_single_record=True)
    if note_to_delete:  
        note_to_delete.deleted_status = True
        db.commit()
        db.refresh(note_to_delete)
        return f'Note with id {note_to_delete.note_id} is deleted.'
    else:
        raise ValueError(f'Note with id: {note_id} does not exist.')

