from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PLACEHOLDER_VALUES = {
    "",
    "replace_me",
    "replace-me",
    "your_api_key_here",
    "your_api_secret_here",
    "your_access_token_here",
    "your_access_token_secret_here",
    "changeme",
}


def _to_bool(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def get_config() -> dict[str, Any]:
    return {
        "twitter_api_key": os.getenv("TWITTER_API_KEY", "").strip(),
        "twitter_api_secret": os.getenv("TWITTER_API_SECRET", "").strip(),
        "twitter_access_token": os.getenv("TWITTER_ACCESS_TOKEN", "").strip(),
        "twitter_access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "").strip(),
        "twitter_username": os.getenv("TWITTER_USERNAME", "MetzinAround").strip(),
        "image_path": os.getenv("IMAGE_PATH", str(BASE_DIR / "lemonitsmonday.png")).strip(),
        "dry_run": _to_bool(os.getenv("DRY_RUN", "false")),
    }


def require_config() -> dict[str, Any]:
    config = get_config()
    missing = []
    for key in [
        "twitter_api_key",
        "twitter_api_secret",
        "twitter_access_token",
        "twitter_access_token_secret",
    ]:
        value = config[key]
        if not value or value.lower() in PLACEHOLDER_VALUES:
            missing.append(key)

    if missing:
        raise RuntimeError(
            "Missing or placeholder X/Twitter credentials: " + ", ".join(missing)
        )

    return config
