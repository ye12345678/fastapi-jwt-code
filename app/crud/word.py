from sqlalchemy.orm import Session
from app.models.word import Word

def create_word_(db: Session, user_id: int, content: str):
    word = Word(user_id=user_id, content=content)
    db.add(word); db.commit(); db.refresh(word)
    return True

def delete_word_(db: Session, word_id: int):
    db.query(Word).filter(Word.id == word_id).delete()
    db.commit()
    return True

def update_word_(db: Session, word_id: int, content: str):
    word = db.query(Word).filter(Word.id == word_id).first()
    if word:
        word.content = content
        db.commit()
        db.refresh(word)
    return word

def get_word_(db: Session, word_id: int):
    return db.query(Word).filter(Word.id == word_id).first()
