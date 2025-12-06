from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def create_user(db: Session, username: str, password: str, phone: str):
    user = User(username=username, hashed_password=hash_password(password), phone=phone)
    db.add(user); db.commit(); db.refresh(user)
    return user

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
