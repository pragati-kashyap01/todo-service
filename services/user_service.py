from sqlalchemy.orm import Session

from db_models import User
from exceptions import UserNotFoundException



# create user


def create_user(
    db: Session,
    name: str,
    email: str | None = None
):
    new_user = User(
        name=name,
        email=email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# get all users


def get_users(
    db: Session,
    q=None,
    skip=0,
    limit=10
):
    query = db.query(User)

    if q:
        query = query.filter(
            (User.name.ilike(f"%{q}%")) |
            (User.email.ilike(f"%{q}%"))
        )

    query = query.offset(skip).limit(limit)

    return query.all()


# =========================
# GET ONE USER
# =========================

def get_user_or_404(
    db: Session,
    user_id: int
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise UserNotFoundException()

    return user


# =========================
# DELETE USER
# =========================

def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()

    return user