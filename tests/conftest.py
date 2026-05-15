import os

import pytest


def _origin_available() -> bool:
    if os.environ.get("ORIGIN_MCP_SKIP_ORIGIN"):
        return False
    try:
        import win32com.client

        win32com.client.Dispatch("Origin.ApplicationSI")
        return True
    except Exception:
        return False


def pytest_configure(config):
    config.addinivalue_line("markers", "origin: requires Origin Pro COM automation")


def pytest_collection_modifyitems(config, items):
    if _origin_available():
        return
    skip_origin = pytest.mark.skip(reason="Origin Pro COM automation is not available")
    for item in items:
        item.add_marker(skip_origin)
