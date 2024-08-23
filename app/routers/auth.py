from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models,utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    This 'OAuth2PasswordRequestForm' is fastapi's built in feature what asks user for credentials and
    return user credentials in a dict object
    {
        "username": "what user enters", "password": "what user enters"
    }
    """
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    print('-------user_credentials: ', user_credentials)
    print('-------user_credentials.username: ', user_credentials.username)
    print('-------user: ', user)
    print('-------user.email: ', user.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    
    # create token
    access_token = oauth2.create_access_token(data={"user_email": user.email})
    """
    this is only user choice what will be send to create_token, here we have only decided user_email,
    we can also user_password, user_role
    """

    # return token
    return {"access_token": access_token, "token_type": "bearer"}