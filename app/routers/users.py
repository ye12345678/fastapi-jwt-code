from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserInfo
from app.db.database import get_db
from app.crud.user import create_user
from app.routers.auth import get_current_user
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register(data: UserCreate, db=Depends(get_db)):
    try:
        _ = create_user(db, data.username, data.password, data.phone)
        return {"msg": "User registered successfully"}
    except SQLAlchemyError as e:
        return {"msg": "Username already exists"}
    except Exception as e:
        return {"msg": f"Registration failed, {e}"}
    

@router.get("/me", response_model=UserInfo)
def me(user=Depends(get_current_user)):
    return user
