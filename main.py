from fastapi import FastAPI
from app.routers import auth, users, word

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(word.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
