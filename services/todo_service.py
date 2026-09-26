from sqlalchemy.orm import Session

from db_models import User, Todo
from exceptions import UserNotFoundException, TodoNotFoundException



# create todo


def create_todo(
    db: Session,
    title: str,
    description: str,
    priority: str,
    due_date: str,
    user_id: int
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise UserNotFoundException()

    new_todo = Todo(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        completed=False,
        user_id=user_id
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo



# get all todos


def get_todos(
    db: Session,
    status=None,
    priority=None,
    user_id=None,
    q=None,
    sort=None,
    skip=0,
    limit=10
):
    query = db.query(Todo)

    # status filter
    if status == "completed":
        query = query.filter(Todo.completed == True)

    elif status == "pending":
        query = query.filter(Todo.completed == False)

    # priority filter
    if priority:
        query = query.filter(
            Todo.priority == priority
        )

    # user filter
    if user_id:
        query = query.filter(
            Todo.user_id == user_id
        )

    # title search
    if q:
        query = query.filter(
            Todo.title.ilike(f"%{q}%")
        )

    # sorting
    if sort == "title":
        query = query.order_by(Todo.title)

    elif sort == "priority":
        query = query.order_by(Todo.priority)

    elif sort == "due_date":
        query = query.order_by(Todo.due_date)

    # pagination
    query = query.offset(skip).limit(limit)

    return query.all()



# get one todo


def get_todo_or_404(db: Session, todo_id: int, user_id: int):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id
    ).first()

    if todo is None:
        raise TodoNotFoundException()

    return todo



# get todos of one user


def get_user_todos(
    db: Session,
    user_id: int
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise UserNotFoundException()

    return db.query(Todo).filter(
        Todo.user_id == user_id
    ).all()



# update todo


def update_todo(
    db: Session,
    todo: Todo,
    title: str,
    description: str,
    priority: str,
    due_date: str,
    user_id: int
):
    if todo.user_id != user_id:
        raise TodoNotFoundException()

    todo.title = title
    todo.description = description
    todo.priority = priority
    todo.due_date = due_date

    db.commit()
    db.refresh(todo)

    return todo



# delete todo


def delete_todo(db: Session, todo: Todo, user_id: int):
    if todo.user_id != user_id:
        raise TodoNotFoundException()

    db.delete(todo)
    db.commit()

    return todo



# complete, uncomplete todo


def complete_todo(
    db: Session,
    todo: Todo,
    completed: bool,
    user_id: int
):
    if todo.user_id != user_id:
        raise TodoNotFoundException()

    todo.completed = completed

    db.commit()
    db.refresh(todo)

    return todo



# search todos


def search_todos(
    db: Session,
    q: str,
    user_id: int
):
    return db.query(Todo).filter(
        Todo.title.ilike(f"%{q}%"),
        Todo.user_id == user_id
    ).all()