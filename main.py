from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from typing import List
import crud as crudsd
import models as models
import schemas

from database import SessionLocal

app = FastAPI()

@app.get("/")
async def docs_redirect():
    response = RedirectResponse(url="/docs")
    return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crudsd.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crudsd.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/email/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = crudsd.get_user_by_email(db, email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crudsd.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crudsd.create_user(db=db, user=user)

@app.put("/users/", response_model=schemas.User)
def update_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crudsd.get_user_by_email(db, email=user.email)
    if db_user:
        return crudsd.update_user(db=db, user=user)
    raise HTTPException(status_code=400, detail="User not Found")