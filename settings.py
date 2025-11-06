from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    model_name: str = Field("gpt-4o-mini", env="U2_MODEL_NAME")
    temperature: float = Field(0.6, env="U2_TEMPERATURE")
    top_p: float = Field(0.9, env="U2_TOP_P")
    search_api_key: str | None = Field(default=None, env="GOOGLE_API_KEY")
    search_engine_id: str | None = Field(default=None, env="GOOGLE_CSE_ID")
    max_retries: int = Field(3, env="U2_MAX_RETRIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
