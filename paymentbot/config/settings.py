from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Pyrogram
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str

    ADMIN: Optional[int]
    PROVIDER_TOKEN: str

    # Antiflood
    MESSAGES = Field(3)
    # Rate limit (N) messages every x seconds
    SECONDS = Field(15)
    # Rate limit x messages every (N) seconds
    CB_SECONDS = Field(15)
    # Rate limit x callback queries every (N) seconds

    class Config:
        case_sensitive: bool = True
        # secrets_dir = "/run/secrets"
        # # https://pydantic-docs.helpmanual.io/usage/settings/#use-case-docker-secrets
        fields = {
            x[0]: {"env": x}
            for x in (
                ["API_ID"],
                ["API_HASH"],
                ["BOT_TOKEN", "TOKEN"],
                ["ADMIN", "OWNER"],
                ["MESSAGES"],
                ["SECONDS"],
                ["CB_SECONDS"],
            )
        }
