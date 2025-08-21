from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "chave_secreta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 90 
    EMAIL_USER: str = 'credenciamentomarka@gmail.com'
    EMAIL_PASSWORD: str ='bszzkdpnrfstsare'
    
settings = Settings()
