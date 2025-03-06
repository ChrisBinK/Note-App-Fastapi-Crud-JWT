from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class NoteModel(Base):
    __tablename__ = 'notes'
    note_id = Column(Integer, primary_key=True, nullable=False, autoincrement='auto', index=True)
    note_title = Column(String(50), nullable=False)
    note_content = Column(String(1500), nullable=False)
    public_status = Column(Boolean, default= False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), nullable=True)
    deleted_status = Column(Boolean, default= False)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('UserModel', back_populates='notes')