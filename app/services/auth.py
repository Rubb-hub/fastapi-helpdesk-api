"""authenticate_user()

register_user()"""

from sqlalchemy.orm import Session

from app.auth.hashing import verify_password
from app.crud.users import get_user_by_login


def authenticate_user(db: Session, user_login: str, password: str):

    user = get_user_by_login(db, user_login)

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
