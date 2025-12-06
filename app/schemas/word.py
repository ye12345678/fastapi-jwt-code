from pydantic import BaseModel


class WordCreate(BaseModel):
    content: str

class WordUpdate(BaseModel):
    word_id: int
    content: str
