from pathlib import Path
from typing import Optional

import typer

from pwdmanager import (
    __version__,
    __app_name__,
    ERRORS,
    config,
    database,
    pwdManager,
    SUCCESS,
    FILE_ERROR,
    DB_READ_ERROR,
)

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt=" Password Database path",
    ),
) -> None:
    """
    initialize the DataBase of passwords
    """
    config_init_code = config.init_app(db_path)
    if config_init_code != SUCCESS:
        typer.secho(
            ERRORS[config_init_code],
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=config_init_code)
    db_init_code = database.init_database(Path(db_path))
    if db_init_code != SUCCESS:
        typer.secho(
            ERRORS[db_init_code],
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=db_init_code)
    typer.secho(
        "Password manager initialized successfully, \n"
        "DB path is: {}".format(db_path),
        fg=typer.colors.GREEN,
    )


def get_pwd_manager() -> pwdManager.PasswordManager:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            "Configuration file not found, please run init command",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=FILE_ERROR)
    if db_path.exists():
        return pwdManager.PasswordManager(db_path=db_path)
    else:
        typer.secho(
            "Database file not found, please run init command",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=DB_READ_ERROR)


def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version number",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """
    A simple password manager
    """
    return
