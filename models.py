from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    priority: str | None = None
    due_date: str | None = None
    user_id: int | None = None

class Config:
    from_attributes = True


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=500)
    priority: Literal["low", "medium", "high"]
    due_date: date
    user_id: int


class TodoComplete(BaseModel):
    completed: bool
    user_id: int


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str | None = None
    password: str = Field(min_length=6)
    
class UserResponse(BaseModel):
    id: int
    name:str
    email:str | None = None
    
class config:
    from_attributes = True
        
class LoginRequest(BaseModel):
    email: str
    password: str