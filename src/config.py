import os
from datetime import datetime

import pytz

try:
    from dotenv import load_dotenv

    load_dotenv()
except:  # noqa
    pass

DEFAULT_TIMEZONE_REGION = "America/Sao_Paulo"
DEFAULT_DATABASE_URL = "postgresql://user:password@localhost:5432/database"


def get_timezone_region() -> str:
    return os.environ.get("TIMEZONE_REGION", DEFAULT_TIMEZONE_REGION)


def generate_now() -> datetime:
    tz = pytz.timezone(get_timezone_region())
    return datetime.now(tz)


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
