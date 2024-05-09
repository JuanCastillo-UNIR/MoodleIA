import os
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict)
from typing import Optional


class ApplicationSettings(BaseSettings):
#FIXME: Commented out for now, depends on azure. 
# class ApplicationSettings(BaseSettings):
#     model_config = SettingsConfigDict(env_nested_delimiter="__", extra="ignore")

#     @classmethod
#     def settings_customise_sources(
#         cls,
#         settings_cls: type[BaseSettings],
#         init_settings: PydanticBaseSettingsSource,
#         env_settings: PydanticBaseSettingsSource,
#         dotenv_settings: PydanticBaseSettingsSource,
#         file_secret_settings: PydanticBaseSettingsSource,
#     ) -> tuple[PydanticBaseSettingsSource, ...]:
#         return (
#             env_settings,
#             AppConfigurationSettingsSource(
#                 settings_cls, os.environ["APP_CONFIGURATION__ENDPOINT"]
#             ),
#         )

    OPEN_AI__AZURE_ENDPOINT: str = "https://proyectoiaopenaiscdev.openai.azure.com/"
    OPEN_AI__API_KEY: str = "c29595dd045545f3b8ae04c999faca04"
    OPEN_AI__API_VERSION: str = "2023-07-01-preview"

    # OPENAI_API_KEY: str = "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"
    # OPENAI_ORG_ID: str = "org-fb2NibLOPT5s0bPa0y2ZVkDI"
    CLAUDE_API_KEY: Optional[str] = None
    PHOENIX_PROJECT_NAME: str = "Contenidos IA"
    PHOENIX_PORT: int = 6006

    SQL_SERVER__HOST: str = "adp-ha.unir.net"
    SQL_SERVER__PORT: int = 22334
    SQL_SERVER__USERNAME: str = "prep.Col"
    SQL_SERVER__PASSWORD: str = "Inn0v4c10n#24"
    SQL_SERVER__NAME: str = "IA"
    
    # SQL_SERVER__CONNECTION_STRING: str
    # SQL_SERVER__HOST: str = "mssql-server-preparador-dev-we-001.database.windows.net"
    # SQL_SERVER__PORT: int = 1433
    # SQL_SERVER__USERNAME: str = "user4defOP7r479X"
    # SQL_SERVER__PASSWORD: str = "v3lllscr37-244saafD-wd33434DLz"
    # SQL_SERVER__NAME: str = "preparador"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

#     SECURITY__JWT__KEY: str = Field("xe9FBxDRzz00SEZmGAxP7dOXGttDVPlZ")
#     SECURITY__JWT__ALGORITHM: str = Field("HS256")
#     SECURITY__JWT__ISSUER: str = Field("asesor.ia")
#     SECURITY__JWT__AUDIENCE: str = Field("asesor")

    # GLOBAL__ENVIRONMENT: str
    # ARCHETYPE__LOGGING_LEVEL: str
    # ARCHETYPE__GREET_TO: str
    # SQL_SERVER__HOST: str = Field("sql-server")
    # SQL_SERVER__PORT: int = Field(1433)
    # SQL_SERVER__USERNAME: str = Field("sa")
    # SQL_SERVER__PASSWORD: str = Field("Password1")
    # SQL_SERVER__NAME: str = Field("master")
    # APPLICATION_INSIGHTS__CONNECTION_STRING: str