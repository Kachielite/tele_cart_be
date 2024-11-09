from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    # Configuring Pydantic to load variables from the .env file
    model_config = SettingsConfigDict(env_file=".env")

# Instantiate settings to load the environment variables
settings = Settings()
