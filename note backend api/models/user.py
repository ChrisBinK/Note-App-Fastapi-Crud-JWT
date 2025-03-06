''''''
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

ACCESS_LEVEL = 0 # DEFAULT ACCESS LEVEL FOR ALL USERS

class RoleModel(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement='auto', index=True)
    role_name = Column(String(15), nullable=False)
    active_status = Column(Boolean, default= True)
    role_description = Column(String(50), nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    access_level = Column(Integer, default = ACCESS_LEVEL)
    users = relationship('UserModel', back_populates='roles')


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement='auto', index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    gender = Column(String(7), nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    roles = relationship('RoleModel', back_populates='users')
    password = Column(String(500))
    email = Column(String(50))
    password_reset_date = Column(DateTime(timezone=True), onupdate=func.now())
    is_verified = Column(Boolean, default =False, nullable=False)
    notes = relationship('NoteModel', back_populates='users')

    
