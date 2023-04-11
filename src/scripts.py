import subprocess
import sys

from dotenv import load_dotenv

argv = sys.argv[1:]


def lint():
    if argv and argv[0] == "check":
        subprocess.run(["poetry", "run", "black", "--check", "src"])
        subprocess.run(["poetry", "run", "isort", "--check-only", "src"])
    else:
        subprocess.run(["poetry", "run", "black", "src"])
        subprocess.run(["poetry", "run", "isort", "src"])


def precommit():
    try:
        subprocess.run(
            [
                "find",
                ".",
                "-name",
                "'.DS_Store'",
                "-type",
                "f",
                "-exec",
                "rm",
                "-f",
                "{}",
                "+",
            ]
        )
    except:
        pass
    lint()


def notebook():
    subprocess.run(["poetry", "run", "jupyter", "notebook"])


def setup():
    subprocess.run(["poetry", "run", "pre-commit", "install"])
    try:
        subprocess.run(
            [
                "poetry run python -m ipykernel install --user --name=pokemon_identification --display-name='Pokemon Identification'"
            ]
        )
    except:
        print("Failed to install ipykernel")


if __name__ == "__main__":
    load_dotenv()
    ignore_warnings()
