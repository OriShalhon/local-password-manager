from pathlib import Path
from typing import NamedTuple, Dict, Any, List

from pwdmanager.database import DataBaseHandler
from pwdmanager import SUCCESS, ID_ERROR


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
            "id": str(len(read.passwords) + 1),
        }
        read.passwords.append(password_data)
        write = self._db_handler.write_passwords(read.passwords)
        return Password(password_data, write.error)

    def get_passwords(self) -> List[Password.password]:
        read = self._db_handler.read_db()
        return read.passwords

    def get_password_by_id(self, password_id: str) -> Password:
        read = self._db_handler.read_db()
        if read.error:
            return Password({}, read.error)
        for password in read.passwords:
            if password["id"] == password_id:
                return Password(password, SUCCESS)
        return Password({}, ID_ERROR)

    def get_password_by_name(self, name: str) -> List[Password.password]:
        read = self._db_handler.read_db()
        if read.error:
            return read.passwords
        passwords = []
        for password in read.passwords:
            if password["name"] == name:
                passwords.append(password)
        return passwords

    def remove_password_by_id(self, password_id: str) -> Password:
        read = self._db_handler.read_db()
        if read.error:
            return Password({}, read.error)
        for password in read.passwords:
            if password["id"] == password_id:
                read.passwords.remove(password)
                write = self._db_handler.write_passwords(read.passwords)
                return Password(password, write.error)
        return Password({}, ID_ERROR)

    def remove_all(self) -> Password:
        write = self._db_handler.write_passwords([])
        return Password({}, write.error)
