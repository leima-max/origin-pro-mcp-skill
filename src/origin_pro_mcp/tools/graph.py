from pathlib import Path
import time

from ..app import mcp
from ..origin_connection import get_origin, execute_labtalk

PLOT_TYPES = {
    "scatter": 201,
    "line": 200,
    "line+symbol": 202,
    "column": 203,
    "bar": 204,
    "area": 205,
    "histogram": 206,
    "box": 207,
    "contour": 208,
    "3d_scatter": 209,
    "3d_surface": 210,
    "pie": 212,
    "bubble": 228,
}

EXPORT_FORMATS = {
    "png": "png",
    "jpg": "jpg",
    "jpeg": "jpg",
    "tif": "tif",
    "tiff": "tif",
    "bmp": "bmp",
    "emf": "emf",
    "eps": "eps",
    "pdf": "pdf",
    "svg": "svg",
}


def _quote_labtalk(value: str) -> str:
    return value.replace('"', '\\"')


def _normalize_export_path(file_path: str, format: str) -> tuple[Path, str]:
    out = Path(file_path).expanduser()
    requested_format = (format or "").strip().lower().lstrip(".")
    suffix_format = out.suffix.lower().lstrip(".")
    export_format = EXPORT_FORMATS.get(suffix_format) or EXPORT_FORMATS.get(requested_format or "png")
    if export_format is None:
        supported = ", ".join(sorted(EXPORT_FORMATS))
        raise ValueError(f"Unsupported export format '{format}'. Supported: {supported}")
    if not out.suffix or EXPORT_FORMATS.get(suffix_format) != export_format:
        out = out.with_suffix(f".{export_format}")
    return out, export_format


def _wait_for_export(file_path: Path, timeout_seconds: float = 8.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        if file_path.exists() and file_path.stat().st_size > 0:
            return True
        time.sleep(0.25)
    return file_path.exists() and file_path.stat().st_size > 0


@mcp.tool()
def create_graph(
    graph_name: str,
    data_book: str,
    data_sheet: str,
    x_col: int,
    y_col: int,
    plot_type: str = "scatter",
    y_error_col: int = 0,
    title: str = ""
) -> str:
    """Create a graph from worksheet data.

    Args:
        graph_name: Name for the graph window
        data_book: Source workbook name
        data_sheet: Source sheet name
        x_col: X column number (1-based)
        y_col: Y column number (1-based)
        plot_type: scatter, line, line+symbol, column, bar, area, histogram,
                   box, contour, pie, bubble
        y_error_col: Optional Y error column number (1-based, 0=none)
        title: Optional graph title

    Returns:
        Created graph name
    """
    o = get_origin()
    ptype = PLOT_TYPES.get(plot_type, 202)

    # FIX: COM CreatePage(3, name, "origin") creates a page where plotxy
    # cannot resolve [name]Layer1, so the plot silently never appears.
    # Use LabTalk to create a real graph window instead. NOTE: in COM
    # automation mode Origin ignores window renaming (win -rn / page.name$
    # / win -t graph <name> all fail), so we always use the auto-assigned
    # window name (GraphN) and return it to the caller. We must also
    # route plotxy to Layer1 explicitly with ogl:=, otherwise plotxy
    # creates a new Layer2 and leaves Layer1 empty (breaking
    # FindGraphLayer("[Graph1]Layer1") for subsequent tools).
    if not execute_labtalk("win -t graph;"):
        return "Failed to create graph window"
    actual_name = o.ActivePage.Name
    execute_labtalk(f"win -a {actual_name};")

    data_ref = f"[{data_book}]{data_sheet}!({x_col},{y_col})"
    if y_error_col > 0:
        data_ref = f"[{data_book}]{data_sheet}!({x_col},{y_col},{y_error_col})"

    if not execute_labtalk(f"plotxy iy:={data_ref} plot:={ptype} ogl:=[{actual_name}]Layer1;"):
        return f"Failed to plot data into {actual_name}: plotxy returned false"

    if title:
        execute_labtalk(f'label -n title -s "{title}"; title.x = 50; title.y = 95;')

    return f"Created graph: {actual_name} ({plot_type})"

@mcp.tool()
def add_plot_to_graph(
    graph_name: str,
    data_book: str,
    data_sheet: str,
    x_col: int,
    y_col: int,
    plot_type: str = "scatter",
    y_error_col: int = 0
) -> str:
    """Add another data series to an existing graph.

    Args:
        graph_name: Existing graph name
        data_book: Source workbook name
        data_sheet: Source sheet name
        x_col: X column number (1-based)
        y_col: Y column number (1-based)
        plot_type: Plot type (scatter, line, line+symbol, etc.)
        y_error_col: Optional Y error column (1-based, 0=none)

    Returns:
        Success message
    """
    ptype = PLOT_TYPES.get(plot_type, 202)
    data_ref = f"[{data_book}]{data_sheet}!({x_col},{y_col})"
    if y_error_col > 0:
        data_ref = f"[{data_book}]{data_sheet}!({x_col},{y_col},{y_error_col})"

    # FIX: in Origin 2024 COM automation, the LabTalk `addplot` command
    # is blocked (returns false), but `plotxy` with explicit ogl:=Layer1
    # APPENDS a new series to Layer1 instead of replacing it. So we
    # use plotxy+ogl for add too.
    if not execute_labtalk(f"win -a {graph_name}; plotxy iy:={data_ref} plot:={ptype} ogl:=[{graph_name}]Layer1;"):
        return f"Failed to add plot to {graph_name}: plotxy returned false"
    return f"Added {plot_type} plot to {graph_name}"

@mcp.tool()
def set_axis_labels(
    graph_name: str,
    x_label: str = "",
    y_label: str = "",
    title: str = ""
) -> str:
    """Set axis labels and title for a graph.

    Args:
        graph_name: Graph name
        x_label: X axis label
        y_label: Y axis label
        title: Graph title

    Returns:
        Success message
    """
    # FIX: rebuild labels first so stale axis titles from previous
    # styling (e.g. apply_publication_style) do not stack/overlap.
    execute_labtalk(f"win -a {graph_name}; label -r;")
    if x_label:
        execute_labtalk(f'xb.text$ = "{x_label}";')
    if y_label:
        execute_labtalk(f'yl.text$ = "{y_label}";')
    if title:
        execute_labtalk(f'label -n title -s "{title}"; title.x = 50; title.y = 95;')
    return f"Updated labels for {graph_name}"

@mcp.tool()
def set_axis_range(
    graph_name: str,
    x_min: float = None,
    x_max: float = None,
    y_min: float = None,
    y_max: float = None
) -> str:
    """Set axis range for a graph.

    Args:
        graph_name: Graph name
        x_min: X axis minimum (None=auto)
        x_max: X axis maximum (None=auto)
        y_min: Y axis minimum (None=auto)
        y_max: Y axis maximum (None=auto)

    Returns:
        Success message
    """
    execute_labtalk(f"win -a {graph_name};")
    if x_min is not None:
        execute_labtalk(f"layer.x.from = {x_min};")
    if x_max is not None:
        execute_labtalk(f"layer.x.to = {x_max};")
    if y_min is not None:
        execute_labtalk(f"layer.y.from = {y_min};")
    if y_max is not None:
        execute_labtalk(f"layer.y.to = {y_max};")
    return f"Set axis range for {graph_name}"

@mcp.tool()
def export_graph(
    graph_name: str,
    file_path: str,
    format: str = "png",
    width: int = 600,
    height: int = 400,
    dpi: int = 300
) -> str:
    """Export a graph to an image file.

    Args:
        graph_name: Graph name to export
        file_path: Full Windows output path (e.g., C:\\Users\\fig1.png)
        format: Image format: png, jpg, tif, bmp, emf, eps, pdf, svg
        width: Reserved for API compatibility; Origin uses the active page export settings
        height: Reserved for API compatibility
        dpi: Reserved for API compatibility

    Returns:
        Path to exported file
    """
    try:
        output_path, export_format = _normalize_export_path(file_path, format)
    except ValueError as e:
        return f"Export failed: {e}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    graph = _quote_labtalk(graph_name)
    folder = _quote_labtalk(str(output_path.parent))
    filename = _quote_labtalk(output_path.stem)

    execute_labtalk(f'win -a "{graph_name}";')
    command = (
        f'expGraph type:={export_format} '
        f'path:="{folder}" filename:="{filename}" '
        f'overwrite:=replace export:=specified pages:="{graph}";'
    )

    if not execute_labtalk(command):
        return f"Export failed: Origin expGraph returned false for {graph_name}"

    if not _wait_for_export(output_path):
        return f"Export failed: no file produced at {output_path}"

    size = output_path.stat().st_size
    if size < 1000:
        return f"Export failed: output too small ({size} bytes) at {output_path}"

    return f"Exported to: {output_path} ({size} bytes)"
