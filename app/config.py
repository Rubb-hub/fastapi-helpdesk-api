from pydantic_settings import BaseSettings, SettingsConfigDict

# Comprobar que ENV_FILE HAY PUESTO OKO


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        #env_file=".env.local",
        extra="ignore")


settings = Settings()  # type: ignore[call-arg]
