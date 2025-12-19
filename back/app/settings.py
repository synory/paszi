from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    hash_scheme: str = "argon2"
    secret_key: str = "CHANGE_ME"
    app_env: str = "docker"
    port: int = 8000

    argon2_time_cost: int = 2
    argon2_memory_cost: int = 102400
    argon2_parallelism: int = 8

    class Config:
        env_file = ".env"

settings = Settings()
