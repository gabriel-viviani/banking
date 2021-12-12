from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from functools import lru_cache
from typing import Iterator
from uuid import UUID
import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from fastapi_utils.session import FastAPISessionMaker

from .config import get_database_url

logger = logging.getLogger(__name__)
Base = declarative_base()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    return FastAPISessionMaker(get_database_url())


def get_db() -> Iterator[Session]:
    try:
        return _get_fastapi_sessionmaker().get_db()
    except Exception as err:
        logger.error(msg=str(err))
        raise HTTPException(status_code=500, detail="Error at database level")


application = FastAPI()
