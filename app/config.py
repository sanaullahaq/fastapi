from pydantic_settings import BaseSettings


"""
This class is for working with OS environment variables.

For example those variables we can not put in the code files because of security issues or they are confedential,
then we will set them in the OS envronment(edit system environment variables).

This class will fetch the env variables based on its attributes names(case-insensetive) and will also validate types (will apply type casting if needed).
For the default values no validations will be applicable.

Most important this class will make sure that all the OS env variables are set else it will throw error.
***But default all the attributes will be returned as str***

***In the development we can use the .env file rather setting the variables in the OS environment.
***But in the production we have to set the variables in OS environment
"""
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings()





# BaseSettings class lives in pydantic_settings,
# Need to install pip install pydantic-settings
# to import from pydantic_settings import BaseSettings