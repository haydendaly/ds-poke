import subprocess
import sys


def main():
    subprocess.run(["poetry", "run", "black", "src"])
