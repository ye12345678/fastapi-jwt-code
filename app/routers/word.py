from fastapi import APIRouter, Depends
from app.schemas.word import WordCreate
from app.db.database import get_db
from app.crud.word import create_word_, delete_word_, update_word_, get_word_
from app.routers.auth import get_current_user

router = APIRouter(prefix="/word", tags=["Word"])

@router.post("/create")
def create_word(data: WordCreate, db=Depends(get_db), user__=Depends(get_current_user)):
    try:
        _ = create_word_(db, user__.id, data.content)
        return {"msg": "Word create successfully"}
    except Exception as e:
        return {"msg": f"failed: {e}"}

@router.delete("/delete/{word_id}")
def delete_word(word_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    try:
        _ = delete_word_(db, word_id)
        return {"msg": "Word deleted successfully"}
    except Exception as e:
        return {"msg": f"failed: {e}"}

@router.put("/update/{word_id}")
def update_word(word_id: int, data: WordCreate, db=Depends(get_db), user=Depends(get_current_user)):
    try:
        word = update_word_(db, word_id, data.content)
        return {"msg": "Word updated successfully", "word": word}
    except Exception as e:
        return {"msg": f"failed: {e}"}  
    
@router.get("/get/{word_id}")
def get_word(word_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    try:
        word = get_word_(db, word_id)
        return {"word": word}
    except Exception as e:
        return {"msg": f"failed: {e}"}
