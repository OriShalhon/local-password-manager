from pathlib import Path
from typing import NamedTuple, Dict, Any

from pwdmanager.database import DataBaseHandler


class Password(NamedTuple):
    password: Dict[str, Any]
    error: int


class PasswordManager:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DataBaseHandler(db_path=db_path)

    def add(self, name: str, password: str) -> Password:
        read = self._db_handler.read_db()
        if read.error:
            return Password({}, read.error)
        password_data = {
            "name": name,
            "password": password,
            "id": str(len(read.data) + 1),
        }
        read.data.append(password_data)
        write = self._db_handler.write_passwords(read.data)
        return Password(password_data, write.error)
