from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')		#url point to from where users can get token

#SECRECT_KEY		#A random string - length is not a matter
#ALGORITHM
#Expiration_Time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
	to_encode = data.copy()
	# expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})

	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
		id: str = payload.get('user_id')		# while encoding the token, we have used 'user_id', so after decoding 'user_id' can be retreived
		# https://jwt.io/ decodes jwt token

		if not id:
			raise credentials_exception
		
		# print('id: ', id)
		return schemas.TokenData(id=str(id))
	except JWTError:
		raise credentials_exception
	
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
	credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
									   detail=f"Could not validate credentials",
									   headers={"WWW-Authenticate": "Bearer"})
	token = verify_access_token(token, credentials_exception)
	# print('token: ', token)
	
	return db.query(models.User).filter(models.User.id == token.id).first()
