"""Legacy entry point — runs the MCP server directly with `python server.py`.

For uvx/pip install, use `origin-pro-mcp` command instead.
"""
import sys
import os

# Add src/ to path so the package can be imported without installing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from origin_pro_mcp.app import main

if __name__ == "__main__":
    main()
