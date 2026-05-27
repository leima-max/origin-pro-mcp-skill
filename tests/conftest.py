import os

import pytest


def _origin_available() -> bool:
    if os.environ.get("ORIGIN_MCP_SKIP_ORIGIN"):
        return False
    if os.environ.get("ORIGIN_MCP_RUN_ORIGIN") != "1":
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
    skip_origin = pytest.mark.skip(
        reason="Origin Pro COM tests are opt-in; set ORIGIN_MCP_RUN_ORIGIN=1 to run them"
    )
    for item in items:
        if "origin" in item.keywords:
            item.add_marker(skip_origin)
