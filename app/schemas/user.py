import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: int
    username: str
    phone: str
    create_at: datetime.datetime
