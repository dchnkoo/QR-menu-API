from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

# for peoduction set DEBUG = False
DEBUG = False


# DATABASE
DATABASE="postgresql+asyncpg://test:test@localhost:5435/test"
DATABASE_SYNC="postgresql://test:test@localhost:5435/test"


# DOMAIN - USE FOR QR-codes GENERATE
DOMAIN = "http://127.0.0.1:8000"


# JWT
from random import randint

SECRET_KEY = "".join([chr(randint(33, 125)) for _ in range(70)])


# LOGGNIG
import logging

logger = logging # don't rename variable

logger.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s',
                   filename=BASE_DIR / 'app.log', filemode='w')


# app init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='QR-menu System'
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*'],
)


# ADMIN

    # Tables per page
TABLES_PER_PAGE = 10