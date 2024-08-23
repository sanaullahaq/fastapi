from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


"""
since we will use this pydantic model to return response.
but in our case our response is a sqlalchemy model but pydantic model expects a dictionary,
that why we added 'orm_mode = True' in the meta 'Config' class
-----------------------------------------------------------------------
| In pydantic v1 'orm_mode' is now renamed to 'from_attributes' in v2 |
-----------------------------------------------------------------------
"""


class PostBase(BaseModel):
	title: str
	content: str
	published: bool = True			# If the user does not provide published value the default will be True
	# rating: Optional[int] = None  # Optional with default None

class PostCreate(PostBase):
	pass

class Post(PostBase):
	id: int
	created_at: datetime

	class Config:
		# orm_mode = True
		from_attributes = True

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class UserOut(BaseModel):
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		# orm_mode = True
		from_attributes = True

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None