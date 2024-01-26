import hashlib
from ...settings import logger


class trash:
    """Цей обьект для мусорних методів в цьому додатку"""

    def get_hash(self, string: str) -> str:
        h = hashlib.sha256(string.encode()).hexdigest()
        logger.info(f"{h[:10]} hash created")
        return h
    
    def parse_user_data(self, data: dict) -> dict:
        return {k: v for k, v in data.items() if k not in ['password', 'hashf', 'token'] and v is not None}
    