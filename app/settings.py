from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

# DATABASE
DATABASE = "sqlite:///" + str(BASE_DIR) + "/db.sqlite3"


# DOMAIN - USE FOR QR-codes GENERATE
DOMAIN = "http://127.0.0.1:8000"


# JWT
SECRET_KEY = "bvuwrvboUEQVBBJwerv1343yeqryvqh13315iirqejrivneqinrvng138508357qto"


# LOGGNIG
import logging

logger = logging # don't rename variable

logger.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s',
                   filename=BASE_DIR / 'app.log', filemode='w')


# ADMIN

    # Tables per page
TABLES_PER_PAGE = 10