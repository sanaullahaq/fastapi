from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')		#url point to from where users can get token

#SECRECT_KEY		#A random string - length is not a matter
#ALGORITHM
#Expiration_Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

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

	"""
	We can directly call 'verify_access_token()' rather call it from 'get_current_user()',
	The moto is that we after calling 'verify_access_token()' we will get the token, and
	using the token we'll fetch the user from the db, and can have the user and apply necessary logic.
	"""
	
	return db.query(models.User).filter(models.User.id == token.id).first()
