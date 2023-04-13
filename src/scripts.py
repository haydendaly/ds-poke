import glob
import subprocess
import sys

from dotenv import load_dotenv

argv = sys.argv[1:]


def lint():
    if argv and argv[0] == "check":
        subprocess.run(["black", "--check", "src"])
        subprocess.run(["isort", "--check-only", "src"])
    else:
        subprocess.run(["black", "src"])
        subprocess.run(["isort", "src"])

        for file in glob.glob("src/**/*.py"):
            if "__init__.py" in file:
                continue
            subprocess.run(
                [
                    "autoflake",
                    "--in-place",
                    "--remove-all-unused-imports",
                    file,
                ]
            )
        print("Removed unused imports")


def notebook():
    try:
        subprocess.run(
            [
                "python",
                "-m",
                "ipykernel",
                "install",
                "--user",
                "--name=pokemon_identification",
                "--display-name='Pokemon Identification'",
            ]
        )
    except:
        print("Failed to install ipykernel")
    subprocess.run(["jupyter", "notebook"])


def setup():
    # subprocess.run(["pre-commit", "install"])
    shared_repo = "https://github.com/haydendaly/ds-poke-shared.git"
    subprocess.run(["cd", "./db"])
    try:
        subprocess.run(["git", "clone", shared_repo])
        subprocess.run(["mv", "ds-poke-shared", "shared"])
        subprocess.run(["cd", ".."])
    except:
        print(
            "Failed to clone shared repo, make sure you accepted the invitation to",
            shared_repo,
        )


if __name__ == "__main__":
    load_dotenv()
