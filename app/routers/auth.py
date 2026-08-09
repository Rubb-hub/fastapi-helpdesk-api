
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.database import get_db
from app.schemas import LoginRequest
from app.services.auth import authenticate_user

router = APIRouter()


# ---ENDPOINT LOGIN AUTH --- POST METHOD
@router.post("/auth/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):

    user = authenticate_user(db, credentials.user_login, credentials.password)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(data={"sub": user.user_login, "role": user.role})

    return {
        # "message": f"Welcome {user.name}"
        "access_token": access_token,
        "token_type": "bearer",
    }
