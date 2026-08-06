from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

 
class Settings(BaseSettings): # Pydantic model for application settings, 
    #used to load configuration values from environment variables or a .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    ) # Configuration to specify the .env file and its encoding for loading environment variables
    
    
    database_url : str # Database connection URL, loaded from environment variables
    
    
    secret_key: SecretStr # Secret key used for cryptographic operations, such as signing JWT tokens, loaded from environment variables
    algorithm: str = "HS256" # Algorithm used for cryptographic operations, such as signing JWT tokens, with a default value of "HS256"
    access_token_expire_minutes: int = 30 # Expiration time for access tokens in minutes, with a default value of 30 minutes
    
    max_upload_size_bytes: int = 5 * 1024 * 1024
    
    posts_per_user : int = 5
    posts_per_page: int = 10
        
    reset_token_expire_minutes : int = 60 
    
    mail_server: str = "localhost"
    mail_port: int = 587
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from: str = "noreply@example.com"
    mail_use_tls: bool = True

    frontend_url: str = "http://localhost:8000"


settings = Settings()  # type: ignore[call-arg] # Loaded from .env file
# This line creates an instance of the Settings class, 
# which loads the configuration values from the .env file. 
# The type: ignore[call-arg] comment is used to suppress type checking errors related to the instantiation of the Settings class.