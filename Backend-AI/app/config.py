from pydantic_settings import BaseSettings
class Settings(BaseSettings): # from .env
    # # database settings
    # database_hostname: str
    # database_port : str
    # database_password: str
    # database_name: str
    # database_username: str
    # # oauth2 settings
    # secret_key: str
    # algorithm: str    
    # access_token_expire_minutes: int

    class Config:
        env_file = ".env"
    
settings = Settings()