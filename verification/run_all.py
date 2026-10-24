#!/usr/bin/env python3
"""Run the finite scientific checks; this does not prove the general theorems."""

from pathlib import Path
import subprocess
import sys


def main():
    directory = Path(__file__).resolve().parent
    for name in ("check_channels.py", "check_frontier.py", "check_detectors.py"):
        completed = subprocess.run(
            [sys.executable, str(directory / name)],
            check=False,
        )
        if completed.returncode:
            raise SystemExit(completed.returncode)
    print("All finite scientific checks passed.")


if __name__ == "__main__":
    main()
