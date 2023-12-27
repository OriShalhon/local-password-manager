import json

import pytest
from typer.testing import CliRunner

from pwdmanager import (
    SUCCESS,
)
from pwdmanager import __version__, __app_name__, cli, pwdManager

runner = CliRunner()


test_data1 = {
    "name": "name1",
    "password": "pass1",
    "password_data": {"name": "name1", "password": "pass1", "id": "1"},
}

test_data2 = {
    "name": "name2",
    "password": "pass2",
    "password_data": {"name": "name2", "password": "pass2", "id": "2"},
}


@pytest.fixture
def mock_json_file(tmp_path):
    password = [{"name": "test", "password": "test"}]
    json_file = tmp_path / "test.json"
    with json_file.open("w") as db_file:
        json.dump(password, db_file, indent=4)
    return json_file


@pytest.mark.parametrize(
    "name, password",
    [
        pytest.param(
            test_data1["name"],
            test_data1["password"],
            (test_data1["password_data"], SUCCESS),
        ),
        pytest.param(
            test_data2["name"],
            test_data2["password"],
            (test_data2["password_data"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, name, password, expected_result):
    pwdmanager = pwdManager.PasswordManager(mock_json_file)
    assert pwdmanager.add(name, password) == expected_result
    read = pwdmanager._db_handler.read_db()
    assert len(read.data) == 2


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"
