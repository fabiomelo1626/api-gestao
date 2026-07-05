from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "chave_secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 
    EMAIL_USER: str = 'famiomelo.1626@gmail.com'
    EMAIL_PASSWORD: str ='fabiomelo@1986'
    
settings = Settings()
