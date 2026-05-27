# Origin Pro MCP 技能包

[English](README.md) | 中文说明

Origin Pro MCP 技能包是一个面向 Windows + OriginLab Origin Pro 的 MCP server 与 AI 技能包。它通过 Origin COM 自动化接口 `Origin.ApplicationSI` 让 AI 助手直接控制 Origin：创建工作簿、写入和读取数据、导入 CSV、绘图、应用论文级样式、曲线拟合、执行 LabTalk、导出图像、保存和加载 Origin 项目。

本仓库是已清理的通用包，不包含个人 API key、Zotero 配置、本地 workspace 状态、实验输出文件或带个人信息的 MCP 配置。

## 功能概览

- 通过 `Origin.ApplicationSI` 连接 Origin Pro
- 提供 23 个 MCP 工具，覆盖项目、数据表、绘图、样式、拟合、导出、LabTalk
- 使用 Origin `expGraph` 导出图片，并校验文件是否真实生成
- CSV 导入会尊重指定 workbook 名称，避免 Origin `impasc` 自动生成 sparkline 图页的副作用
- 内置 `skills/publication-figure.md` 论文图工作流
- 内置 pytest 测试；无 Origin 环境会自动跳过 Origin COM 测试

## 环境要求

- Windows
- Origin Pro 2020 或更高版本，并可正常启动
- Python 3.10 或更高版本，必须是 Windows Python，不建议使用 WSL Python
- Python 依赖：`mcp`、`pywin32`、`Pillow`

## 安装

```powershell
git clone https://github.com/leima-max/origin-pro-mcp-skill.git
cd origin-pro-mcp-skill
python -m pip install -e .
```

使用前请先启动 Origin Pro。

## MCP 配置

如果已经安装为 Python 包，可以直接使用命令：

```json
{
  "mcpServers": {
    "origin-pro": {
      "command": "origin-pro-mcp"
    }
  }
}
```

如果想直接运行本地 server 文件：

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

已清理的示例配置见 `examples/mcporter.example.json`。请将 `PATH_TO_REPO` 替换为你自己的仓库路径。

## OpenClaw 配置

安装 Python 包后，把 MCP server 注册到 OpenClaw：

```powershell
openclaw mcp set origin-pro '{"command":"origin-pro-mcp"}'
openclaw mcp show origin-pro
```

如果控制台命令不在 PATH 中，可以直接指向本地 server 文件：

```powershell
openclaw mcp set origin-pro '{"command":"python","args":["-u","PATH_TO_REPO/server.py"]}'
```

为了便于发布到 ClawHub，根目录 `SKILL.md` 已补充 OpenClaw 可识别的 frontmatter，`agents/openai.yaml` 也声明了 `origin-pro` MCP 依赖，方便 UI 侧展示。

## 快速测试

```powershell
python -m pytest -q
```

默认测试只验证包导入和 MCP 工具注册，不会触碰 Origin Pro。依赖 Origin COM 的真实集成测试需要显式开启：

```powershell
$env:ORIGIN_MCP_RUN_ORIGIN="1"; python -m pytest -q
```

只有在 Windows 机器已安装并启动 Origin Pro，且允许测试创建/清空临时项目时，才建议运行该集成测试。

也可以只验证 MCP 工具是否完成注册：

```powershell
python -c "import origin_pro_mcp.server; from origin_pro_mcp.app import mcp; print(len(mcp._tool_manager._tools))"
```

期望输出：`23`。

## 典型使用流程

1. 启动 Origin Pro。
2. 让 AI 创建或导入工作表数据。
3. 从工作表列创建图。
4. 一键应用论文图样式。
5. 需要时执行曲线拟合。
6. 导出图像并检查文件是否生成。

示例工具流程：

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

## MCP 工具清单

项目管理：

- `new_project`
- `save_project`
- `load_project`

数据与工作表：

- `create_worksheet`
- `set_worksheet_data`
- `get_worksheet_data`
- `import_csv_to_worksheet`
- `list_worksheets`

绘图：

- `create_graph`
- `add_plot_to_graph`
- `set_axis_labels`
- `set_axis_range`
- `export_graph`
- `export_all_graphs`

样式：

- `apply_publication_style`
- `set_plot_style`
- `set_graph_font`
- `set_legend`
- `set_tick_style`

分析：

- `curve_fit`
- `list_fitting_functions`

高级：

- `run_labtalk`
- `get_labtalk_variable`

## 注意事项

- Origin COM 只能从 Windows Python 调用。
- 第一次连接 Origin COM 时，如果 Origin 是冷启动，可能需要数秒。
- 如果 Origin 弹出阻塞对话框，MCP 调用可能等待或超时。
- `export_graph` 使用 `expGraph`，其中 `path` 是输出目录，`filename` 是文件名主体；工具会验证导出文件是否存在且大小合理。
- `import_csv_to_worksheet` 使用 Python 解析 CSV，再通过 COM 写入列，避免 `impasc` 自动生成额外 sparkline 图页。

## 安全与清理说明

本通用包刻意排除了：

- 本地 `config/mcporter.json`
- API key、token、密钥文件
- Zotero 或其他第三方连接器配置
- 本地 workspace 记忆、日志和实验输出
- 带个人信息的绝对路径

发布衍生版本前，建议扫描密钥、token、密码、本地连接器名称和机器专用路径。例如：

```powershell
rg -n "key|token|secret|credential|password|local_user_path|connector_specific_env"
```

## 许可证

MIT。原始上游包信息保留在 `pyproject.toml` 元数据与源码说明中。
