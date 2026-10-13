from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


print("Shubham Sharma 23051870")


# ============================================================
# BASE PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(BASE_DIR / ".env")


APP_NAME = os.getenv(
    "APP_NAME",
    "Enterprise AI Decision Intelligence",
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0",
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
)

DEBUG = os.getenv(
    "DEBUG",
    "False",
).lower() == "true"

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()


# ============================================================
# API CONFIGURATION
# ============================================================

API_HOST = os.getenv(
    "API_HOST",
    "127.0.0.1",
)

API_PORT = int(
    os.getenv(
        "API_PORT",
        "8000",
    )
)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if origin.strip()
]


# ============================================================
# DATA DIRECTORIES
# ============================================================

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

DOCUMENTS_DIR = DATA_DIR / "documents"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "enterprise_ai.db"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DATABASE_FILE}",
)


# ============================================================
# LLM CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gpt-4o-mini",
)


# ============================================================
# DIRECTORY INITIALIZATION
# ============================================================

for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    DOCUMENTS_DIR,
    DATABASE_DIR,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )