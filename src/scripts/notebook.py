import sys
import subprocess


def main():
    try:
        subprocess.run(
            ["poetry run python -m ipykernel install --user --name=pokemon_identification --display-name='Pokemon Identification'"])
    except:
        print("Failed to install ipykernel")
    subprocess.run(["poetry", "run", "jupyter", "notebook"])
