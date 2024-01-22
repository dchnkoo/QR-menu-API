import base64


class trash:
    """Цей класс для методів які не грають
    головну роль в цьому додатку"""

    def get_hash(self, string: str) -> str:
        return base64.b64encode(string).decode()