import json
import unittest
import pytest
from typer.testing import CliRunner
import string

from pwdmanager import (
    SUCCESS,
    __version__,
    __app_name__,
    cli, pwdManager
)

runner = CliRunner()


@pytest.fixture
def mock_json_file(tmp_path):
    password = [{"name": "test", "password": "test", "id": "1"}]
    json_file = tmp_path / "test.json"
    with json_file.open("a") as db_file:
        json.dump(password, db_file, indent=4)
    return json_file


def test_add(mock_json_file):
    test_data1 = {
        "name": "name1",
        "password": "pass1",
        "expected_return": {"name": "name1", "password": "pass1", "id": "2"},
    }

    test_data2 = {
        "name": "name2",
        "password": "pass2",
        "expected_return": {"name": "name2", "password": "pass2", "id": "3"},
    }

    pwdmanager = pwdManager.PasswordManager(mock_json_file)
    assert pwdmanager.add(test_data1["name"], test_data1["password"]).password == test_data1["expected_return"]
    assert pwdmanager.add(test_data2["name"], test_data2["password"]).password == test_data2["expected_return"]
    read = pwdmanager._db_handler.read_db()
    assert len(read.passwords) == 3


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"


def test_password_without_uppercase():
    result = runner.invoke(cli.app, ['generate', '-n test', '--no-uppercase'])
    assert result.exit_code == 0
    generated_password = result.output.strip().split(": ")[1]
    assert not (any(char.isupper() for char in generated_password))


def test_password_without_lowercase():
    result = runner.invoke(cli.app, ['generate', '-n test', '--no-lowercase'])
    assert result.exit_code == 0
    generated_password = result.output.strip().split(": ")[1]
    assert not (any(char.islower() for char in generated_password))


def test_password_without_digits():
    result = runner.invoke(cli.app, ['generate', '-n test', '--no-digits'])
    assert result.exit_code == 0
    generated_password = result.output.strip().split(": ")[1]
    assert not (any(char.isdigit() for char in generated_password))


def test_password_without_special():
    result = runner.invoke(cli.app, ['generate', '-n test', '--no-special'])
    assert result.exit_code == 0
    generated_password = result.output.strip().split(": ")[1]
    assert not (any(char in string.punctuation for char in generated_password))
