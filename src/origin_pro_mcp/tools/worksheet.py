import csv
import json
from pathlib import Path

from ..app import mcp
from ..origin_connection import get_origin, execute_labtalk

@mcp.tool()
def create_worksheet(book_name: str, sheet_name: str = "Sheet1") -> str:
    """Create a new workbook with a worksheet in Origin.

    Args:
        book_name: Name for the new workbook
        sheet_name: Name for the sheet (default: Sheet1)

    Returns:
        Created workbook name
    """
    o = get_origin()
    name = o.CreatePage(2, book_name, "origin")
    if sheet_name != "Sheet1":
        execute_labtalk(f'page.active$ = "Sheet1"; wks.name$ = "{sheet_name}";')
    return f"Created workbook: [{name}]{sheet_name}"

@mcp.tool()
def set_worksheet_data(
    book_name: str,
    sheet_name: str,
    columns: str,
    column_names: str = ""
) -> str:
    """Write data to an Origin worksheet.

    Args:
        book_name: Workbook name (e.g., "Book1")
        sheet_name: Sheet name (e.g., "Sheet1")
        columns: JSON array of arrays, each inner array is a column of data.
                 Example: [[1,2,3],[4,5,6]] for 2 columns with 3 rows
        column_names: Optional comma-separated column names (e.g., "X,Y,Error")

    Returns:
        Success message
    """
    o = get_origin()
    target = f"[{book_name}]{sheet_name}"
    cols = json.loads(columns)

    for i, col_data in enumerate(cols):
        float_data = [float(x) for x in col_data]
        o.PutWorksheet(target, float_data, 0, i)

    if column_names:
        names = [n.strip() for n in column_names.split(",")]
        execute_labtalk(f'win -a {book_name};')
        for i, name in enumerate(names):
            execute_labtalk(f'wks.col{i+1}.lname$ = "{name}";')

    return f"Set {len(cols)} columns x {len(cols[0])} rows in {target}"

@mcp.tool()
def get_worksheet_data(book_name: str, sheet_name: str) -> str:
    """Read data from an Origin worksheet.

    Args:
        book_name: Workbook name
        sheet_name: Sheet name

    Returns:
        JSON object with column data
    """
    o = get_origin()
    target = f"[{book_name}]{sheet_name}"
    data = o.GetWorksheet(target)
    if data is None:
        return json.dumps({"error": f"Worksheet {target} not found"})

    if len(data) == 0:
        return json.dumps({"columns": []})

    num_cols = len(data[0])
    columns = []
    for c in range(num_cols):
        columns.append([row[c] for row in data])

    return json.dumps({"columns": columns})

@mcp.tool()
def import_csv_to_worksheet(
    file_path: str,
    book_name: str = "",
    delimiter: str = ","
) -> str:
    """Import a CSV/text file into an Origin worksheet.

    Args:
        file_path: Full Windows path to the file (e.g., C:\\Users\\data.csv)
        book_name: Optional workbook name. Auto-generated if empty.
        delimiter: Column delimiter (default: comma)

    Returns:
        Name of the created workbook
    """
    path = Path(file_path)
    if not path.exists():
        return f"Import failed: file not found: {file_path}"

    csv_delimiter = "\t" if delimiter in ("\\t", "\t") else delimiter
    if len(csv_delimiter) != 1:
        return f"Import failed: delimiter must be a single character, got {delimiter!r}"

    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = [row for row in csv.reader(f, delimiter=csv_delimiter) if any(cell.strip() for cell in row)]

    if not rows:
        return f"Import failed: no data rows found in {file_path}"

    width = len(rows[0])
    if width == 0 or any(len(row) != width for row in rows):
        return "Import failed: ragged rows are not supported"

    header = []
    data_rows = rows
    try:
        [[float(cell) if cell.strip() else float("nan") for cell in row] for row in rows]
    except ValueError:
        header = [cell.strip() for cell in rows[0]]
        data_rows = rows[1:]

    if not data_rows:
        return f"Import failed: no numeric data rows found in {file_path}"

    try:
        numeric_rows = [
            [float(cell) if cell.strip() else float("nan") for cell in row]
            for row in data_rows
        ]
    except ValueError as e:
        return f"Import failed: non-numeric data encountered: {e}"

    columns = [[row[col] for row in numeric_rows] for col in range(width)]

    o = get_origin()
    target_name = book_name or path.stem
    actual_book = o.CreatePage(2, target_name, "origin")
    sheet_name = "Sheet1"
    execute_labtalk(f'win -a {actual_book};')

    for i, col_data in enumerate(columns):
        o.PutWorksheet(f"[{actual_book}]{sheet_name}", col_data, 0, i)

    for i, name in enumerate(header):
        if name:
            safe_name = name.replace('"', '\\"')
            execute_labtalk(f'wks.col{i+1}.lname$ = "{safe_name}";')

    return f"Imported to workbook: {actual_book}"

@mcp.tool()
def list_worksheets() -> str:
    """List all open workbooks and worksheets in Origin.

    Returns:
        JSON list of workbooks with their sheets
    """
    result = []

    execute_labtalk(
        'string __mcp_pages$ = ""; '
        'doc -e W { __mcp_pages$ = __mcp_pages$ + page.name$ + "|workbook;"; }; '
        'doc -e P { __mcp_pages$ = __mcp_pages$ + page.name$ + "|graph;"; };'
    )
    raw = get_origin().LTStr("__mcp_pages$")
    for entry in raw.split(";"):
        if not entry:
            continue
        name, _, page_type = entry.partition("|")
        if name and page_type:
            result.append({"book": name, "type": page_type})

    return json.dumps(result)
