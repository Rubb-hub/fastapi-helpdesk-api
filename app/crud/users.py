"""get_user_by_login()

create_user()
"""

from sqlalchemy.orm import Session

from app.models import User


# ----SQL FUNCTION -- GET USER ---ENDPOINT LOGIN AUTH
def get_user_by_login(db: Session, user_login: str):

    return db.query(User).filter(User.user_login == user_login).first()


def create_user(db: Session, user: User):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user
