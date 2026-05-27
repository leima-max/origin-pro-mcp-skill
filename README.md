# Origin Pro MCP Skill Package

English | [中文说明](README.zh-CN.md)

Origin Pro MCP Skill Package is a Windows-first MCP server and Codex/Claude-style skill package for controlling OriginLab Origin Pro through COM automation. It lets an AI assistant create workbooks, write and read worksheet data, import CSV files, build graphs, apply publication-style formatting, run curve fitting, execute LabTalk, export figures, and save/load Origin projects.

This repository is a sanitized, reusable package. It does not contain personal API keys, Zotero configuration, local workspace state, generated experiment outputs, or machine-specific MCP configuration.

## Features

- Origin Pro COM automation through `Origin.ApplicationSI`
- 23 MCP tools for project, worksheet, graph, style, fitting, export, and LabTalk workflows
- File-verified graph export using Origin `expGraph`
- CSV import that respects the requested Origin workbook name and avoids Origin `impasc` side effects
- Publication figure workflow in `skills/publication-figure.md`
- Pytest coverage with Origin-aware skip behavior for machines without Origin installed

## Requirements

- Windows
- Origin Pro 2020 or newer, installed and able to start
- Python 3.10 or newer, using Windows Python rather than WSL Python
- Python packages: `mcp`, `pywin32`, `Pillow`

## Install

```powershell
git clone https://github.com/leima-max/origin-pro-mcp-skill.git
cd origin-pro-mcp-skill
python -m pip install -e .
```

Start Origin Pro before calling tools that need COM automation.

## MCP Configuration

Use either the installed console command:

```json
{
  "mcpServers": {
    "origin-pro": {
      "command": "origin-pro-mcp"
    }
  }
}
```

Or run the local server file directly:

```json
{
  "mcpServers": {
    "origin-pro": {
      "command": "python",
      "args": ["-u", "PATH_TO_REPO/server.py"]
    }
  }
}
```

A sanitized example is available at `examples/mcporter.example.json`.

## OpenClaw Setup

After installing the Python package, register the MCP server in OpenClaw:

```powershell
openclaw mcp set origin-pro '{"command":"origin-pro-mcp"}'
openclaw mcp show origin-pro
```

If the console script is not available on PATH, point OpenClaw at the checked-out server file:

```powershell
openclaw mcp set origin-pro '{"command":"python","args":["-u","PATH_TO_REPO/server.py"]}'
```

For ClawHub publication, the root `SKILL.md` contains OpenClaw-readable frontmatter and `agents/openai.yaml` declares the `origin-pro` MCP dependency for UI surfaces.

## Quick Smoke Test

```powershell
python -m pytest -q
```

The default test run verifies package import and MCP tool registration without touching Origin Pro. Origin-dependent COM tests are skipped unless you opt in:

```powershell
$env:ORIGIN_MCP_RUN_ORIGIN="1"; python -m pytest -q
```

Use the opt-in integration run only on a Windows machine with Origin Pro installed and started.

You can also verify tool registration without starting Origin:

```powershell
python -c "import origin_pro_mcp.server; from origin_pro_mcp.app import mcp; print(len(mcp._tool_manager._tools))"
```

Expected output: `23`.

## Typical AI Workflow

1. Start Origin Pro.
2. Ask the assistant to create or import worksheet data.
3. Create a graph from worksheet columns.
4. Apply publication style in one call.
5. Fit a curve if needed.
6. Export figures and verify that files were created.

Example tool flow:

```python
new_project()
create_worksheet(book_name="Data", sheet_name="Sheet1")
set_worksheet_data(
    book_name="Data",
    sheet_name="Sheet1",
    columns="[[0,1,2,3],[0.02,0.08,0.18,0.36],[0.11,0.42,0.90,1.62]]",
    column_names="Bias,Dark,Light"
)
create_graph(graph_name="Fig1", data_book="Data", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line+symbol")
add_plot_to_graph(graph_name="Fig1", data_book="Data", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line+symbol")
apply_publication_style(
    graph_name="Fig1",
    x_label="Voltage (V)",
    y_label="Current density (mA cm^-2)",
    x_min=0,
    x_max=3,
    y_min=0,
    y_max=2,
    legend_entries="Dark,Light",
    legend_position="top-left"
)
export_graph(graph_name="Fig1", file_path="OUTPUT_DIR/Fig1.png")
```

## MCP Tools

Project:

- `new_project`
- `save_project`
- `load_project`

Worksheet and data:

- `create_worksheet`
- `set_worksheet_data`
- `get_worksheet_data`
- `import_csv_to_worksheet`
- `list_worksheets`

Graphing:

- `create_graph`
- `add_plot_to_graph`
- `set_axis_labels`
- `set_axis_range`
- `export_graph`
- `export_all_graphs`

Styling:

- `apply_publication_style`
- `set_plot_style`
- `set_graph_font`
- `set_legend`
- `set_tick_style`

Analysis:

- `curve_fit`
- `list_fitting_functions`

Advanced:

- `run_labtalk`
- `get_labtalk_variable`

## Notes and Known Constraints

- Origin COM only works from Windows Python.
- The first COM connection can take several seconds if Origin is cold-starting.
- If Origin shows a blocking dialog, MCP calls may wait or time out.
- `export_graph` uses `expGraph` with a directory `path` and a separate `filename`; the tool verifies output file existence and size.
- `import_csv_to_worksheet` parses CSV in Python and writes columns through COM to avoid `impasc` auto-generated sparkline graph pages.

## Security and Sanitization

This package intentionally excludes:

- local `config/mcporter.json`
- API keys and token files
- Zotero or other third-party connector settings
- local workspace memory, logs, and generated experiment output
- user-specific absolute paths

Before publishing derived versions, run a secret scan for keys, tokens, passwords, local connector names, and machine-specific paths. For example:

```powershell
rg -n "key|token|secret|credential|password|local_user_path|connector_specific_env"
```

## License

MIT. The original upstream package is credited in `pyproject.toml` project metadata and source history notes.
