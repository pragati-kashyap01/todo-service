from pydantic import BaseModel
class Todo(BaseModel):
    id: int
    title:str
    description:str
    completed: bool
    priority:str
    due_date:str
    created_at:str
    updated_at:str
    
class TodoCreate(BaseModel):
    title: str
    description: str
    priority:str
    due_date:str
    
class TodoComplete(BaseModel):
    completed: bool