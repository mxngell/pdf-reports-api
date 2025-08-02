from pathlib import Path
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000  

    TEMPLATES_DIR: str = "templates"
    TEMPLATE: str = "template.html"
    OUTPUT_DIR: str = "reports_archive"
    LOGS_DIR: str = "logs"

    @field_validator("TEMPLATES_DIR", "OUTPUT_DIR", "LOGS_DIR")
    def validate_dirs(cls, value: str):
        if not Path(value).exists():
            raise ValueError(f"Directory '{value}' does not exist")
        return value

    @model_validator(mode="after")
    def validate_template(self):
        if not Path(self.TEMPLATES_DIR).joinpath(self.TEMPLATE).exists():
            raise ValueError(f"Template '{self.TEMPLATE}' does not exist")
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid"
    )

settings = Settings()