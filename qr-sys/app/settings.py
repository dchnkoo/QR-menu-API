from pathlib import Path

from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

DEBUG = False

# DATABASE
if DEBUG:
    DATABASE = "sqlite+aiosqlite:///" + str(BASE_DIR) + "/db.sqlite3"
    DATABASE_SYNC = "sqlite:///" + str(BASE_DIR) + "/db.sqlite3"
else:
    DATABASE_SYNC = os.environ.get("DATABASE_URL_SYNC")
    DATABASE = os.environ.get("DATABASE_URL") # production



# DOMAIN - USE FOR QR-codes GENERATE
DOMAIN = "http://127.0.0.1:8000"


# JWT
SECRET_KEY = os.environ.get("JWT_KEY")


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