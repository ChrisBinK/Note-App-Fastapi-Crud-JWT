from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class RoleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id :int
    role_name:str
    active_status:bool
    role_description:str
    date_created:datetime
    date_updated:datetime
    access_level:int
    
class UserSignUpSchema(BaseModel):
    class Config:
        from_attribute = True
    id: Optional[int]
    first_name: str
    last_name: str
    gender: str
    password: str
    email: EmailStr

    def to_dict(self):
        return self.__dict__

class UserSchema(UserSignUpSchema):
    model_config = ConfigDict(from_attributes=True)
    date_created: datetime
    date_updated : datetime
    is_deleted: bool
    role_id: int
    password_reset_date: datetime
    is_verified: bool
    


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str



