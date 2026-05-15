from mcp.server.fastmcp import FastMCP

mcp = FastMCP("origin-pro")


def main():
    """Entry point for uvx / console_scripts."""
    from . import server  # noqa: F401 — registers all tools
    mcp.run(transport="stdio")
