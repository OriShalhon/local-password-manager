from typer.testing import CliRunner

from pwdmanager import __version__, __app_name__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == f"{__app_name__} version {__version__}\n"

