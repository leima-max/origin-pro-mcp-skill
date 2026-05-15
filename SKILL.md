# Origin Pro MCP Skill / Origin Pro MCP 技能

## English

Use this skill when the user wants to create, edit, style, fit, or export Origin Pro worksheets and figures through the `origin-pro` MCP server.

### Scope

- Create and manage Origin projects.
- Create worksheets, write JSON column arrays, read worksheet data, and import numeric CSV files.
- Create scatter, line, line+symbol, bar, histogram, box, contour, pie, bubble, and selected 3D graph types.
- Apply publication-style formatting with one tool call.
- Run linear and nonlinear curve fitting.
- Execute LabTalk for advanced Origin operations.
- Export verified image files from Origin graph pages.

### Prerequisites

- Windows with Origin Pro 2020 or newer.
- Windows Python 3.10 or newer.
- Package installed with `python -m pip install -e .`.
- MCP server configured as `origin-pro`.
- Origin Pro started before COM-dependent operations.

### Default Workflow

1. Confirm Origin Pro is running.
2. Use `new_project` only when it is acceptable to clear the current Origin session.
3. Load data with `create_worksheet` + `set_worksheet_data` or `import_csv_to_worksheet`.
4. Use `create_graph` and `add_plot_to_graph`.
5. Use `apply_publication_style` for journal-ready formatting.
6. Use `curve_fit` when fitting is requested.
7. Use `export_graph` or `export_all_graphs`, then verify the returned file path and size.

### Safety Rules

- Do not include local API keys, token files, Zotero settings, or workspace-specific MCP config in shared outputs.
- Ask before calling `new_project` if the user may have unsaved Origin work.
- Treat a successful export as valid only when the tool reports a generated file with non-trivial size.
- If a tool hangs, check whether Origin is showing a modal dialog.

## 中文

当用户希望通过 `origin-pro` MCP server 创建、编辑、排版、拟合或导出 Origin Pro 工作表和图像时，使用本技能。

### 能力范围

- 创建和管理 Origin 项目。
- 创建工作表、写入 JSON 列数组、读取工作表数据、导入数值型 CSV 文件。
- 创建 scatter、line、line+symbol、bar、histogram、box、contour、pie、bubble 和部分 3D 图。
- 一键应用论文图样式。
- 执行线性和非线性曲线拟合。
- 通过 LabTalk 执行高级 Origin 操作。
- 从 Origin 图页导出经过文件校验的图片。

### 前置条件

- Windows，安装 Origin Pro 2020 或更高版本。
- Windows Python 3.10 或更高版本。
- 已执行 `python -m pip install -e .`。
- MCP server 已配置为 `origin-pro`。
- 依赖 COM 的操作前请先启动 Origin Pro。

### 默认流程

1. 确认 Origin Pro 正在运行。
2. 只有在可以清空当前 Origin 会话时才调用 `new_project`。
3. 使用 `create_worksheet` + `set_worksheet_data` 或 `import_csv_to_worksheet` 加载数据。
4. 使用 `create_graph` 和 `add_plot_to_graph` 绘图。
5. 使用 `apply_publication_style` 完成论文图样式。
6. 需要拟合时调用 `curve_fit`。
7. 使用 `export_graph` 或 `export_all_graphs` 导出，并检查返回的路径和文件大小。

### 安全规则

- 不要在共享输出中包含本地 API key、token 文件、Zotero 设置或工作区专用 MCP 配置。
- 如果用户可能有未保存的 Origin 工作，调用 `new_project` 前先确认。
- 只有当导出工具报告生成了非空文件时，才视为导出成功。
- 如果工具卡住，先检查 Origin 是否弹出了模态对话框。
