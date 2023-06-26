from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # for password hasing purpose, here `bcrypt` is the hasing algorithm

def hash(password: str):
    return pwd_context.hash(password)