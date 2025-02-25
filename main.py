from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi import Depends, FastAPI

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