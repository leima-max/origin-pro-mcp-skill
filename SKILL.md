---
name: origin-pro-mcp
description: "Control OriginLab Origin Pro through the origin-pro MCP server for worksheets, graphs, materials characterization, photodetector metrics, publication styling, fitting, LabTalk, and verified figure export. Use for Origin Pro/OriginLab automation, scientific plotting, Tauc/XRD/PL/Raman/XPS/TEM/AFM/Hall figures, I-V/EQE/responsivity/D*/response-time/noise plots, or OpenClaw MCP setup for Origin."
homepage: https://github.com/leima-max/origin-pro-mcp-skill
metadata:
  {
    "openclaw":
      {
        "os": ["win32"],
        "requires": { "bins": ["python"] },
      },
  }
---

# Origin Pro MCP Skill / Origin Pro MCP 技能

## English

Use this skill when the user wants to create, edit, style, fit, analyze, or export Origin Pro worksheets and figures through the `origin-pro` MCP server.

This skill is a general scientific plotting package with added materials-science and photodetector workflows. For detailed figure recipes, read `skills/publication-figure.md` before making final figures.

### Scope

- Create and manage Origin projects.
- Create worksheets, write JSON column arrays, read worksheet data, and import numeric CSV files.
- Create scatter, line, line+symbol, bar, histogram, box, contour, pie, bubble, and selected 3D graph types.
- Apply publication-style formatting with one tool call.
- Run linear and nonlinear curve fitting.
- Execute LabTalk for advanced Origin operations.
- Export verified image files from Origin graph pages.
- Build materials characterization figures: Tauc/absorption, XRD, Raman, PL, XPS/UPS, TEM/FFT, AFM/roughness, Hall and mobility plots.
- Build photodetector figures: I-V, rectification ratio, photocurrent, EQE, responsivity, detectivity, noise, response time, light-intensity dependence, and device statistics.
- Support device-agnostic photodetector workflows that can be adapted to different material systems and device stacks.

### Prerequisites

- Windows with Origin Pro 2020 or newer.
- Windows Python 3.10 or newer.
- Package installed with `python -m pip install -e .`.
- MCP server configured as `origin-pro`.
- Origin Pro started before COM-dependent operations.

### OpenClaw Setup

Install the package from the checked-out skill folder:

```powershell
python -m pip install -e .
```

Register the MCP server with OpenClaw:

```powershell
openclaw mcp set origin-pro '{"command":"origin-pro-mcp"}'
openclaw mcp show origin-pro
```

If the console command is not on PATH, register the local server file instead:

```powershell
openclaw mcp set origin-pro '{"command":"python","args":["-u","PATH_TO_REPO/server.py"]}'
```

Run the fast package check without Origin:

```powershell
python -m pytest -q
```

Run real Origin COM integration tests only when Origin Pro is installed, started, and disposable test projects are acceptable:

```powershell
$env:ORIGIN_MCP_RUN_ORIGIN="1"; python -m pytest -q
```

### Default Workflow

1. Confirm Origin Pro is running.
2. Confirm whether `new_project` may clear the current Origin session.
3. Identify the figure class: general graph, materials characterization, or photodetector metric.
4. Collect mandatory metadata: units, sample labels, test conditions, active area or film thickness when relevant, and export target.
5. Load data with `create_worksheet` + `set_worksheet_data` or `import_csv_to_worksheet`.
6. Compute derived columns outside Origin when formulas matter, then write both raw and derived columns where possible.
7. Use `create_graph` and `add_plot_to_graph`.
8. Use `apply_publication_style` first, then fine-tune with axis, legend, tick, plot-style, or LabTalk tools.
9. Use `curve_fit` only on a physically justified region, and report the fit range and model.
10. Use `export_graph` or `export_all_graphs`, then verify the returned file path and size.

### Materials and Photodetector Reporting Rule

Every technical figure should state:

- Goal: what the figure is proving or comparing.
- Operation steps: data transform, plotting tool flow, fitting/export steps.
- Expected result: what a healthy material/device should show.
- Failure criterion: what would make the figure misleading or physically suspicious.
- Next step: the characterization, process adjustment, or device experiment implied by the result.

For photodetectors, interpret results through:

- Band Alignment: junction energetics, contact selectivity, barriers.
- Carrier Dynamics: generation, extraction, recombination, transit, response speed.
- Trap States: leakage, hysteresis, persistent photoconductivity, slow tails.
- Built-in Field: rectification, zero-bias response, reverse-bias enhancement.

### Tool List

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

### Safety Rules

- Do not include local API keys, token files, Zotero settings, or workspace-specific MCP config in shared outputs.
- Ask before calling `new_project` if the user may have unsaved Origin work.
- Treat a successful export as valid only when the tool reports a generated file with non-trivial size.
- If a tool hangs, check whether Origin is showing a modal dialog.
- Do not report D* without a noise definition, Tauc bandgap without the exponent/fit range, or epitaxy without orientation evidence.

## 中文

当用户希望通过 `origin-pro` MCP server 创建、编辑、排版、拟合、分析或导出 Origin Pro 工作表和图像时，使用本技能。

这是一个通用科研绘图技能包，并面向材料表征和光电探测器论文图进行了扩展。制作最终图前，优先阅读 `skills/publication-figure.md` 中的详细模板。

### 能力范围

- 创建和管理 Origin 项目。
- 创建工作表、写入 JSON 列数组、读取工作表数据、导入数值型 CSV 文件。
- 创建 scatter、line、line+symbol、bar、histogram、box、contour、pie、bubble 和部分 3D 图。
- 一键应用论文图样式。
- 执行线性和非线性曲线拟合。
- 通过 LabTalk 执行高级 Origin 操作。
- 从 Origin 图页导出经过文件校验的图片。
- 支持材料表征图：Tauc/吸收、XRD、Raman、PL、XPS/UPS、TEM/FFT、AFM 粗糙度、Hall 和迁移率。
- 支持光电探测器图：I-V、整流比、光电流、EQE、响应度、探测率、噪声、响应时间、光强依赖和器件统计。
- 支持不绑定特定材料体系的光电探测器论文图，可按不同器件结构和材料体系调整。

### 前置条件

- Windows，安装 Origin Pro 2020 或更高版本。
- Windows Python 3.10 或更高版本。
- 已执行 `python -m pip install -e .`。
- MCP server 已配置为 `origin-pro`。
- 依赖 COM 的操作前请先启动 Origin Pro。

### 默认流程

1. 确认 Origin Pro 正在运行。
2. 确认是否允许 `new_project` 清空当前 Origin 会话。
3. 判断图像类型：通用图、材料表征图或光电探测器指标图。
4. 收集必要元数据：单位、样品标签、测试条件、活性面积或膜厚、导出目录。
5. 使用 `create_worksheet` + `set_worksheet_data` 或 `import_csv_to_worksheet` 加载数据。
6. 需要公式计算时先在 Origin 外完成派生列，并尽量保留原始列与派生列。
7. 使用 `create_graph` 和 `add_plot_to_graph` 绘图。
8. 先使用 `apply_publication_style`，再用坐标轴、图例、刻度、曲线样式或 LabTalk 工具微调。
9. 仅在物理上合理的区间进行 `curve_fit`，并报告拟合区间和模型。
10. 使用 `export_graph` 或 `export_all_graphs` 导出，并检查返回的路径和文件大小。

### 材料与器件图汇报规则

每张技术图都应包含：

- 目标：这张图要证明或比较什么。
- 操作步骤：数据变换、绘图工具流、拟合和导出步骤。
- 预期结果：健康材料或器件应呈现什么趋势。
- 失败判据：哪些情况会让图像误导或物理上可疑。
- 下一步：该结果对应的表征、工艺调整或器件实验动作。

光电探测器结果默认从四个维度解释：

- Band Alignment：结能级、接触选择性、界面势垒。
- Carrier Dynamics：光生、分离、输运、复合、响应速度。
- Trap States：漏电、迟滞、持续光电导、慢尾。
- Built-in Field：整流、零偏光伏响应、反偏增强。

### 安全规则

- 不要在共享输出中包含本地 API key、token 文件、Zotero 设置或工作区专用 MCP 配置。
- 如果用户可能有未保存的 Origin 工作，调用 `new_project` 前先确认。
- 只有当导出工具报告生成了非空文件时，才视为导出成功。
- 如果工具卡住，先检查 Origin 是否弹出了模态对话框。
- 不要在没有噪声定义时报告 D*，不要在没有 Tauc 指数/拟合区间时报告带隙，不要在没有取向证据时声称外延。
