from base64 import urlsafe_b64encode
from uuid import uuid4


def generate_filename() -> str:
    """Генерирует уникальное имя файла."""
    return urlsafe_b64encode(uuid4().bytes).decode().rstrip('=')
