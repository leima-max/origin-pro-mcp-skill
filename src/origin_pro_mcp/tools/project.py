from pathlib import Path

from ..app import mcp
from ..origin_connection import get_origin, execute_labtalk

@mcp.tool()
def new_project() -> str:
    """Create a new empty Origin project (closes current without saving)."""
    o = get_origin()
    o.NewProject()
    return "New project created"

@mcp.tool()
def save_project(file_path: str = "") -> str:
    """Save the current Origin project.

    Args:
        file_path: Full Windows path to save (e.g., C:\\Users\\data\\experiment.opju).
                   If empty, saves to current location.

    Returns:
        Save confirmation with path
    """
    o = get_origin()
    if file_path:
        o.Save(file_path)
        return f"Project saved to: {file_path}"
    else:
        o.Save("")
        return "Project saved"

@mcp.tool()
def load_project(file_path: str) -> str:
    """Open an Origin project file.

    Args:
        file_path: Full Windows path to .opj or .opju file

    Returns:
        Success message
    """
    o = get_origin()
    o.Load(file_path)
    return f"Loaded project: {file_path}"

@mcp.tool()
def export_all_graphs(
    output_dir: str,
    format: str = "png",
    dpi: int = 300,
    width: int = 800,
    height: int = 600
) -> str:
    """Export all graphs in the current project to image files.

    Args:
        output_dir: Windows directory path for output files
        format: Image format (png, jpg, tif, emf, eps, pdf, svg)
        dpi: Resolution (default 300)
        width: Width in pixels
        height: Height in pixels

    Returns:
        Confirmation message
    """
    from .graph import export_graph

    out_dir = Path(output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    execute_labtalk(
        'string __mcp_graphs$ = ""; '
        'doc -e P { __mcp_graphs$ = __mcp_graphs$ + page.name$ + "|"; };'
    )
    raw = get_origin().LTStr("__mcp_graphs$")
    graph_names = [name for name in raw.split("|") if name]
    if not graph_names:
        return "Export failed: no graph pages found"

    exported = []
    failures = []
    for graph_name in graph_names:
        target = out_dir / f"{graph_name}.{format.lower().lstrip('.') or 'png'}"
        result = export_graph(graph_name, str(target), format, width, height, dpi)
        if result.startswith("Exported to:"):
            exported.append(str(target))
        else:
            failures.append(f"{graph_name}: {result}")

    if failures:
        return (
            f"Exported {len(exported)} of {len(graph_names)} graphs to {out_dir}. "
            f"Failures: {'; '.join(failures)}"
        )

    return f"Exported {len(exported)} graphs to: {out_dir}"
