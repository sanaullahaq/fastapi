from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    # If the user does not provide published value the default will be True
    published: bool = True
    # rating: Optional[int] = None  # Optional with default None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
    '''
    since we will use this pydantic model to return response.
    but in our case our response is a sqlalchemy model but pydantic model expects a dictionary,
    that why we added `orm_mode=True` in the meta `Config` class
    '''

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password: str