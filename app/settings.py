from pathlib import Path


BASE_DIR = Path(__file__).parent.parent

# DATABASE
DATABASE = "sqlite:///" + str(BASE_DIR) + "/db.sqlite3"