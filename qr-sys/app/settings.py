from pathlib import Path
import json
import os


BASE_DIR = Path(__file__).parent.parent

# for peoduction set DEBUG = False
DEBUG = False

# DATABASE
DATABASE="postgresql+asyncpg://test:test@localhost:5435/test"
DATABASE_SYNC="postgresql://test:test@localhost:5435/test"

# redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# email | if DEBUG = False use docker env with the same constants
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = ...
SENDER_PASSWORD = ...


# DOMAIN - USE FOR QR-codes GENERATE
DOMAIN = "http://qrsystem.source.com"


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

origins = list(json.loads(os.environ.get("CORS_ORIGINS_API"))) if "CORS_ORIGINS_API" in os.environ.keys() else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADMIN

    # Tables per page
TABLES_PER_PAGE = 10

    # LOGO
MAX_WIDTH = 300
MAX_HEIGHT = 300

    # LOGO for QR-code
QR_LOGO_WIDTH = 130
QR_LOGO_HEIGHT = 130

LOGO_OVRL = QR_LOGO_WIDTH + 20
