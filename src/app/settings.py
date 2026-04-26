from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class CommonSettings(BaseSettings):
    # The pydantic-settings automatically maps with field case insensitively
    # No need for:
    #   project_domain: str  = Field(env="PROJECT_DOMAIN")
    # plus that has been changed to:
    #   project_domain: str  = Field(alias="PROJECT_DOMAIN")
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1] / ".env.local",
        env_file_encoding="utf-8",
        validate_by_alias=True,  # for Field(alias = "env_name")
        extra="ignore",
    )


class AppSettings(CommonSettings):
    api_version: str = "1.0.0"
    project_name: str = Field(default="", alias="PROJECT_NAME")
    project_domain: str = Field(default="", alias="PROJECT_DOMAIN")

class DBSettings(CommonSettings):
    db_user: str      = Field(default="", alias="DB_USER")
    db_name: str      = Field(default="", alias="DB_NAME")
    db_host: str      = Field(default="", alias="DB_HOST")
    db_port: str      = Field(default="", alias="DB_PORT")
    db_password: str  = Field(default="", alias="DB_PASSWORD")

    @property
    def db_async_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

class ShopifySettings(CommonSettings):
    shopify_app_cliend_id:str       = Field(default="", alias="SHOPIFY_APP_CLIENT_ID")
    shopify_app_secret:str          = Field(default="", alias="SHOPIFY_APP_SECRET")
    shopify_app_scopes:str          = Field(default="", alias="SHOPIFY_APP_SCOPES")
    shopify_app_redirect_url:str    = Field(default="", alias="SHOPIFY_APP_REDIRECT_URL")


class Settings(CommonSettings):
    app_settings: AppSettings = Field(default_factory=AppSettings)
    db_settings: DBSettings = Field(default_factory=DBSettings)
    shopify_settings: ShopifySettings = Field(default_factory=ShopifySettings)


def import_settings():
    return Settings()