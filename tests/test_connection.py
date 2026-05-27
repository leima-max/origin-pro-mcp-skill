import subprocess, sys

import pytest

pytestmark = pytest.mark.origin

def test_origin_connection():
    result = subprocess.run(
        [sys.executable, "-c",
         "import win32com.client; o = win32com.client.Dispatch('Origin.ApplicationSI'); print('OK')"],
        capture_output=True, text=True, timeout=30
    )
    assert result.stdout.strip() == "OK", result.stderr
