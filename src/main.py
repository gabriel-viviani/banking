import logging
from fastapi import FastAPI

from src.entrypoint.router import api_router
from src.repository.database import init_db


logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_router)

init_db()
