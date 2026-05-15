from .app import mcp

from .tools import labtalk  # noqa: F401
from .tools import worksheet  # noqa: F401
from .tools import graph  # noqa: F401
from .tools import style  # noqa: F401
from .tools import fitting  # noqa: F401
from .tools import project  # noqa: F401

if __name__ == "__main__":
    mcp.run(transport="stdio")
