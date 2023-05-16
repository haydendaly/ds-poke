import glob
import os
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
            if "__init__.py" in file or "archive/" in file:
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
    try:
        subprocess.run(["git", "clone", shared_repo, "./db/shared"])
    except:
        print(
            "Failed to clone shared repo, make sure you accepted the invitation to",
            shared_repo,
        )


def update_cgc():
    shared_repo = "https://github.com/haydendaly/ds-poke-shared-cgc.git"
    if os.path.exists("./db/shared-cgc"):
        subprocess.run(["git", "pull"], cwd="./db/shared-cgc")
    else:
        try:
            subprocess.run(["git", "clone", shared_repo, "./db/shared-cgc"])
        except:
            print(
                "Failed to clone shared repo, make sure you accepted the invitation to",
                shared_repo,
            )


def docker():
    subprocess.run(["docker-compose", "up", "-d"])


def docker_build():
    if len(argv) < 1:
        print("Usage: poetry run build <service_name> <dev?>")
        return
    service_name = argv[0]
    build_context = f"./src/services/{service_name}"
    entrypoint_module = f"src.services.{service_name}:main"
    is_dev = argv and argv[1] == "dev"

    subprocess.run(
        [
            "docker",
            "build",
            "-t",
            service_name,
            "--build-arg",
            f"ENTRYPOINT_MODULE={entrypoint_module}",
            "Dockerfile" + (".dev" if is_dev else ""),
            build_context,
        ],
    )


# def typecheck():
#     subprocess.run(["mypy", "src"])


if __name__ == "__main__":
    load_dotenv()
