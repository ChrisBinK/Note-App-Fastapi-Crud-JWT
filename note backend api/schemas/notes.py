from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class NoteSchema(BaseModel):
    note_id:int
    note_title: str # 50
    note_content:str #1500 
    public_status:bool
    date_created:Optional[datetime]
    date_updated:Optional[datetime]
    deleted_status:Optional[bool]
    user_id: int
