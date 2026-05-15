from ..app import mcp
from ..origin_connection import execute_labtalk, get_lt_var, get_lt_str

@mcp.tool()
def run_labtalk(script: str) -> str:
    """Execute a LabTalk script in Origin Pro.

    Use this for any Origin operation not covered by other tools.
    LabTalk is Origin's built-in scripting language.

    Args:
        script: LabTalk script to execute

    Returns:
        Success/failure message
    """
    success = execute_labtalk(script)
    return f"Executed {'successfully' if success else 'with errors'}: {script}"

@mcp.tool()
def get_labtalk_variable(name: str) -> str:
    """Get the value of a LabTalk variable.

    Args:
        name: Variable name. Use $ suffix for strings (e.g., 'str$')

    Returns:
        Variable value as string
    """
    if name.endswith("$"):
        return get_lt_str(name)
    else:
        return str(get_lt_var(name))
