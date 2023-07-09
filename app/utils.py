from passlib.context import CryptContext

# for password hasing purpose, here `bcrypt` is the hasing algorithm
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


'''
Basically `pwd_context.verify(plain_password, hashed_password)` will convert the plain password into a hashed password and will match with hashed password sent and will return true/false
'''
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
