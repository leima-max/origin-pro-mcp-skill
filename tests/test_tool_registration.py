from origin_pro_mcp.app import mcp
import origin_pro_mcp.server  # noqa: F401


def test_tool_registration_count():
    assert len(mcp._tool_manager._tools) == 23
