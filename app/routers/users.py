from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
	prefix='/users',
	tags=['Users']			# This will group the paths operations based on this tags in the Swagger UI
)
# this router connects path-operations lives in this file with main.py

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

	# Check if the user already exists
	# user_exists = db.query(models.User).filter(models.User.email == user.email).first()
	# if user_exists:
	# 	raise HTTPException(status_code=status.HTTP_409_CONFLICT,
	# 						detail="User already exists")
	
	# If user doesn't exist, create and save the user
	user.password = utils.hash(user.password)			#hash the password - user.password
	# new_user = models.User(**user.dict())
	new_user = models.User(**user.model_dump())			# '**' can be used when calling a function to unpack a dictionary into keyword arguments.
	db.add(new_user)
	db.commit()
	db.refresh(new_user)

	return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.id == id).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
							detail=f'User with id: {id} was not found')
	return user