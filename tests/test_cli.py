"""CLI rejects unsafe hosts before any network fetch."""

import subprocess
import sys


def test_cli_rejects_private_address() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "dealforge.cli",
            "discover-url",
            "http://127.0.0.1:9000/private",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert "Rejected unsafe URL" in completed.stderr
    assert "127.0.0.1" not in completed.stdout
