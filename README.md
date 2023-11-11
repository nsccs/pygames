# Pygames

A mono-repo for a collection of different games created with the Pygame library.

## Get Started

This repository's structure is as follows:

```shell
pygames (root)
  --game_title (game root)
    --src (application code directory)
      --class_directories (as needed)
      --main.py (application entry point)
      --requirements.py (packages required to develop the game)
  --game_title
    --(follow same pattern)
```

Each game directory is its own project.

## Setup

Install Python 3.12

Fork the directory and set the upstream repository (see [Workbook: Contribute](https://nsccs.github.io/git_and_github_workshop/contribute.html))

Move into the directory of the game you wish to contribute to

```shell
cd <game_directory_name>
```

Create a virtual environment to install packages into

```shell
python3.12 -m venv .venv
```

Activate the environment
```shell
# macOS/Linux
source .venv/bin/activate
# PowerShell (Windows)
.venv\Scripts\Activate.ps1
```

Upgrade pip

```shell
python3.12 -m pip install --upgrade pip
```

Install required game packages

```shell
pip install -r requirements.txt
```

Start the game

```shell
python src/main.py
```

You are all set! If you have not yet taken one of the club's GitHub workshops or want a refresher visit our [Workbook: Git & GitHub Chapter](https://nsccs.github.io/git_and_github_workshop/index.html)

## Contributing

Feel free to start your own game or contribute to an existing one.

Not sure where to start? Visit the [Issues](https://github.com/nsccs/pygames/issues) section for a list of tickets that will help get you started.

See a bug or want to request a feature or change? Create an issue!

### Workflow

Main is protected and will require a PR and approval to merge into main.

## Game List

1. Asteroid clone

