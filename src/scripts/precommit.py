import sys
import subprocess


def main():
    subprocess.run(
        ["find . -name '.DS_Store' -type f -exec rm -f {} +"])
    subprocess.run(["poetry", "run", "lint"])
