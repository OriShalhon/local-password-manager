import json
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from pwdmanager import (
    SUCCESS,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
    JSON_ERROR,
)

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_pwd_manager.json"
)


def get_database_path(config_file: Path) -> Path:
    config_parser = ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    try:
        db_path.write_text("[]")
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    data: List[Dict[str, Any]]
    error: int


class DataBaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_db(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def write_passwords(self, data: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(data, db, indent=4)
            return DBResponse(data, SUCCESS)
        except OSError:  # Catch file IO problems
            return DBResponse(data, DB_WRITE_ERROR)

    def append_password(self, data: Dict[str, Any]) -> DBResponse:
        read = self.read_db()
        if read.error:
            return DBResponse([], read.error)
        read.data.append(data)
        return self.write_passwords(read.data)
