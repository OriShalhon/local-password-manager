from pathlib import Path
from typing import Optional
import string
import random
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


@app.command()
def add(
        name: str = typer.Option(
            ..., "--name", "-n", prompt="Password name", help="Password name"
        ),
        password: str = typer.Option(
            ...,
            "--password",
            "-p",
            prompt="Password",
            help="Password to be stored",
            confirmation_prompt=True,
            hide_input=True,
        ),
) -> None:
    """
    Add a password to the database
    """
    pwd_manager = get_pwd_manager()
    password = pwd_manager.add(name, password)
    if password.error:
        typer.secho(
            "Error while adding password: {}".format(ERRORS[password.error]),
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=password.error)
    typer.secho(
        "Password added successfully, \n"
        "Password ID is: {}".format(password.password["id"]),
        fg=typer.colors.GREEN,
    )


@app.command(name="list")
def list_passwords() -> None:
    """
    List all passwords in the database
    """
    pwd_manager = get_pwd_manager()
    passwords = pwd_manager.get_passwords()
    if not passwords:
        typer.secho(
            "No passwords found",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=DB_READ_ERROR)
    typer.secho("Password list:", fg=typer.colors.BLUE, bold=True)
    columns = ("ID  ",
               "| Name  ",
               "| Password  ",
               )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for password in passwords:
        typer.secho(
            "{id}   | {name}   | {password}".format(
                id=password["id"],
                name=password["name"],
                password=password["password"],
            ),
            fg=typer.colors.BLUE,
        )


@app.command()
def generate(
        name: str = typer.Option(
            ..., "--name", "-n", prompt="Password name", help="Password name"
        ),
        length: int = typer.Option(
            16,
            "--length",
            "-l",
            help="Password length",
            show_default=True,
        ),
        uppercase: bool = typer.Option(
            True,
            "--no-uppercase",
            "-u",
            help="Exclude uppercase letters",
            show_default=True,
        ),
        lowercase: bool = typer.Option(
            True,
            "--no-lowercase",
            "-c",
            help="Exclude lowercase letters",
            show_default=True,
        ),
        digits: bool = typer.Option(
            True,
            "--no-digits",
            "-d",
            help="Exclude digits",
            show_default=True,
        ),
        special: bool = typer.Option(
            True,
            "--no-special",
            "-s",
            help="Exclude special characters",
            show_default=True,
        ),
        save_to_db: bool = typer.Option(
            False,
            "--save",
            help="Save password to database",
            show_default=True,
        ),
) -> None:
    """
    Generate a random password
    """
    characters = ''

    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if digits:
        characters += string.digits
    if special:
        characters += string.punctuation

    # Ensure at least one character type is selected
    if not any([uppercase, lowercase, digits, special]):
        typer.secho(
            "At least one character type should be selected.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    # Generate password
    password = ''.join(random.choice(characters) for _ in range(length))

    typer.secho(
        "Generated password: {}".format(password),
        fg=typer.colors.GREEN,
    )

    if save_to_db:
        pwd_manager = get_pwd_manager()
        password = pwd_manager.add(name, password)
        if password.error:
            typer.secho(
                "Error while adding password: {}".format(ERRORS[password.error]),
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=password.error)
        typer.secho(
            "Password added successfully, \n"
            "Password ID is: {}".format(password.password["id"]),
            fg=typer.colors.GREEN,
        )


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
