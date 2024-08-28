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

class UserOut(BaseModel):
	id: int
	email: EmailStr
	created_at: datetime

	class Config:
		# orm_mode = True
		from_attributes = True

class Post(PostBase):
	id: int
	created_at: datetime
	owner_id: int		#this field can be added to the 'PostBase' schema as well, but adding here is more efficient
						#In case of PostCreate it is not efficient that user will provide his own id(owner_id) while creating a post
						#While creating post owner_id is being fetched from the token
	owner: UserOut

	class Config:
		# orm_mode = True
		from_attributes = True

class UserCreate(BaseModel):
	email: EmailStr
	password: str

class UserLogin(BaseModel):
	email: EmailStr
	password: str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None