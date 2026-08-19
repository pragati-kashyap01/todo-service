from fastapi import FastAPI, HTTPException
from storage import load_data, save_data
from models import TodoCreate,TodoComplete
from datetime import datetime

app = FastAPI()

@app.get("/todos")
def get_todos():
    data = load_data()
    return data["todos"]

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    data = load_data()

    for todo in data["todos"]:
        if todo["id"] == todo_id:
            return todo
    
    raise HTTPException(status_code = 404, detail ="Todo not found")

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    data = load_data()
    
    now = datetime.now().isoformat()
    
    new_todo = {
        "id": data["next_id"],
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "priority": todo.priority,
        "due_date": todo.due_date,
        "created_at": now,
        "updated_at": now
    }
    
    data["todos"].append(new_todo)
    data["next_id"]+= 1
    
    save_data(data)
    
    return new_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    data = load_data()
    
    for todo in data["todos"]:
        if todo["id"]== todo_id:
            data["todos"].remove(todo)
            save_data(data)
            return{"message": "todo deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Todo not found")
    
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoCreate):
    data = load_data()
    
    for existing_todo in data["todos"]:
        if existing_todo["id"] == todo_id:
            existing_todo["title"] = todo.title
            existing_todo["description"] = todo.description
            existing_todo["priority"] = todo.priority
            existing_todo["due_date"]= todo.due_date
            existing_todo["updated_at"] = datetime.now().isoformat()
            
            save_data(data)
            return existing_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.patch("/todos/{todo_id}/complete")
def complete_todo(todo_id: int, update:TodoComplete):
    data = load_data()
    
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["completed"]= update.completed
            todo["updated_at"] = datetime.now().isoformat()
            
            save_data(data)
            return todo
    
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/search")
def search_todos(q:str):
    data = load_data()
    
    results = []
    
    for todo in data["todos"]:
        if q.lower() in todo["title"].lower() or q.lower() in todo["description"].lower():
            results.append(todo)
            
    return results