from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import select
from models.user import UserModel
from schemas.user import UserSignUpSchema, UserSchema
from utils.authentication import get_password_hash
from datetime import datetime

from environs import env
env.read_env()

from enum import Enum
class DatabaseFunction(Enum):
    CREATE = 1 
    READ = 2
    UPDATE=3 
    QUERY =4

def get_user_by_field(model_field:InstrumentedAttribute, value:str, db:Session):
    ''' Get user record by a field name specified as parameter'''
    return db.scalars(select(UserModel).where( model_field == value)).first()


def create_user_db(user:UserSignUpSchema, db:Session):
    '''Create a user if the email does not exists'''
   
    existing_user = get_user_by_field(UserModel.email, user.email, db)
    if existing_user:
        raise ValueError('User email already exists.')
    hash_password = get_password_hash(user.password)
    new_user = UserModel(first_name = user.first_name,last_name = user.last_name,
                gender= user.gender,password = hash_password, email = user.email, role_id = int(env('USER_ROLE_ID')))
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserSignUpSchema(**new_user.__dict__)

def update_user_db(user:UserSignUpSchema, db:Session):
    existing_user  = get_user_by_field(UserModel.id , user.id, db)
   
    if  existing_user:
        existing_user.date_updated = datetime.now()
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        for field in ['first_name', 'last_name', 'gender', 'email', 'password']:
            setattr(existing_user, field, getattr(user,field))
        db.commit()
        db.refresh(existing_user)
        return existing_user
    else:
        raise ValueError(f'User with id {user.id} does not exist.')


def delete_user_db(user_id: int, db:Session):
    existing_user  = get_user_by_field(UserModel.id , user_id, db)
    if existing_user:
        existing_user.is_deleted = True
        db.commit()
        db.refresh(existing_user)
        return f'User with id{existing_user.id} is deleted.'
    else:
        raise ValueError(f'User with id {user_id} does not exist.')
    
def get_all_user_db(db:Session):
    all_users = db.scalars(select(UserModel).order_by(UserModel.created_at)).all()