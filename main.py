import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from models import UserCreate, TodoCreate, TodoComplete, UserResponse, Todo
from database import engine, Base, SessionLocal
from services import user_service
from services import todo_service
from exceptions import UserNotFoundException, TodoNotFoundException




Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# exception handlers


@app.exception_handler(UserNotFoundException)
def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "User not found"}
    )


@app.exception_handler(TodoNotFoundException)
def todo_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Todo not found"}
    )


# database session


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



# user crud



# create user
@app.post("/users", status_code=201, response_model=UserResponse, tags = ["users"])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating user: %s", user.name)
    return user_service.create_user(
        db,
        user.name
    
    )


# get all user
@app.get("/users", response_model=list[UserResponse],tags =["users"])
def get_users(
    db: Session = Depends(get_db)
):
    return user_service.get_users(db)


# get one user
@app.get("/users/{user_id}", response_model=UserResponse, tags =["users"])
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.get_user_or_404(
        db,
        user_id
    )


# delete user
@app.delete("/users/{user_id}", tags = ["users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_or_404(
        db,
        user_id
    )

    user_service.delete_user(
        db,
        user
    )

    return {
        "message": "User deleted successfully"
    }



# todo crud



# create todo
@app.post("/todos", status_code=201, response_model=Todo, tags =["todos"])
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    logger.info("Creating todo: %s", todo.title)
    
    return todo_service.create_todo(
        db,
        todo.title,
        todo.description,
        todo.priority,
        todo.due_date,
        todo.user_id
    )


# get all todos
# filtering+ search + sorting + pagination
@app.get("/todos", response_model=list[Todo], tags =["todos"])
def get_todos(
    status: str = None,
    priority: str = None,
    user_id: int = None,
    q: str = None,
    sort: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return todo_service.get_todos(
        db,
        status,
        priority,
        user_id,
        q,
        sort,
        skip,
        limit
    )

# search todos
@app.get("/todos/search", response_model=list[Todo], tags=["todos"])
def search_todos(
    q: str,
    db: Session = Depends(get_db)
):
    return todo_service.search_todos(
        db,
        q
    )


# get one todo
@app.get("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def get_todo(
    todo_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return todo_service.get_todo_or_404(
        db,
        todo_id,
        user_id
    )





# get todos of one user
@app.get("/users/{user_id}/todos", response_model=list[Todo], tags=["todos"])
def get_user_todos(
    user_id: int,
    db: Session = Depends(get_db)
):
    return todo_service.get_user_todos(
        db,
        user_id
    )


# update todo
@app.put("/todos/{todo_id}", response_model=Todo, tags=["todos"])
def update_todo(
    todo_id: int,
    todo: TodoCreate,
    db: Session = Depends(get_db)
):
    existing_todo = todo_service.get_todo_or_404(
        db,
        todo_id
    )

    return todo_service.update_todo(
        db,
        existing_todo,
        todo.title,
        todo.description,
        todo.priority,
        todo.due_date,
        todo.user_id
    )


# delete todo
@app.delete("/todos/{todo_id}", tags=["todos"])
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    todo = todo_service.get_todo_or_404(
        db,
        todo_id
    )

    todo_service.delete_todo(
        db,
        todo
    )

    return {
        "message": "Todo deleted successfully"
    }


#  complete , uncomplete todo
@app.patch("/todos/{todo_id}/complete",response_model=Todo, tags=["todos"])
def complete_todo(
    todo_id: int,
    update: TodoComplete,
    db: Session = Depends(get_db)
):
    todo = todo_service.get_todo_or_404(
    db,
    todo_id,
    update.user_id
    )
    
    return todo_service.complete_todo(
        db,
        todo,
        update.completed,
        update.user_id
    )