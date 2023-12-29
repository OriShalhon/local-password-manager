# Password Manager CLI

## Introduction

This project is a command-line interface (CLI) password manager.
It has two main functionalities, the first is to generate passwords based on the user's input,
and the second is to securely store and manage passwords locally on the user's computer.

## Installation

To install this project, follow these steps:

1. Clone the repository:

```sh
git clone <repository_url>
```

2. Navigate to the project directory:

```sh
cd pwd_manager_CLI
```

3. Activate python environment

```sh
python -m venv venv

.\venv\Scripts\activate
```

4. Install the package:

```sh
pip install -r requirements.txt
```

## Testing

To run the tests for this project, use the following command:

```sh
python -m pytest .\tests\
```

## password manager usage

Here are some examples of how to use the password manager:

- To initialize the password manager:

```sh
python -m pwdmanager init
```

- To add a password:

```sh
python -m pwdmanager add --name <password_name> --password <password>
```

- To get a password:

```sh
python -m pwdmanager get --id <password_id>
python -m pwdmanager get --name <password_name>
```

- To remove a password:

```sh
python -m pwdmanager remove --id <password_id>
```

by adding --help flag to any of the comments you can see the full list of options.

## Password generator usage

Here are some examples of how to use the password generator:

- `--length` or `-l` - the length of the password (default 16)
- `--no-uppercase` or `-u` - exclude uppercase letters
- `--no-lowercase` or `-c` - exclude lowercase letters
- `--no-digits` or `-d` - exclude digits
- `--no-special` or `-s` - exclude symbols
- `--save` - save the password to the password manager

upon generating a password - a name for the password will be prompted, if the `--save` flag is used,
the password will be saved to the password manager.

```sh
python -m pwdgenerator generate -u -d
```

## Contributing

Contributions are welcome. Please submit a pull request or open an issue to discuss the changes you want to make.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please reach out to us at <ori.shalhon@gmail.com>.

