from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    gender: str
    country: str
    isActive: bool