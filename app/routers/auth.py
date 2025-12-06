from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.db.database import get_db
from app.schemas.user import UserLogin
from app.core.security import verify_password, create_access_token
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.token_blacklist import add_token_to_blacklist, is_token_blacklisted
from app.crud.user import get_user

router = APIRouter(tags=["Auth"])
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/login")
def login(data: UserLogin, db=Depends(get_db)):
    user = get_user(db, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid username or password")
    return {"access_token": create_access_token({"sub": user.username}), "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2)):
    """将token加入黑名单"""
    add_token_to_blacklist(token)
    return {"msg": "User logged out successfully"}

def get_current_user(token: str = Depends(oauth2), db=Depends(get_db)):
    """验证token有效性和黑名单状态"""
    if is_token_blacklisted(token):
        raise HTTPException(401, "Token has been revoked")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Token invalid or expired")
    user = get_user(db, username)
    if not user:
        raise HTTPException(404, "User not found")
    return user
