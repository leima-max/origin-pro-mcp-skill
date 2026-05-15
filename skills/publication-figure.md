# Publication Figure Workflow / 论文图工作流

## English

Use this workflow when the user asks for a publication-quality Origin Pro figure.

### Before Starting

Confirm:

- data source: direct arrays, CSV file, or existing Origin workbook
- figure type: scatter, line, line+symbol, bar, histogram, or other
- number of datasets
- axis labels and units
- target journal or style preference
- export directory and file format

If the user does not specify a style, default to a clean journal style: Arial, bold axis titles, inward ticks, closed frame, no grid lines, white background, and colorblind-aware colors.

### Recommended Tool Flow

1. `create_worksheet` and `set_worksheet_data`, or `import_csv_to_worksheet`.
2. `create_graph`.
3. `add_plot_to_graph` for additional datasets.
4. `apply_publication_style`.
5. `curve_fit` if a fit is requested.
6. `export_graph` and verify the returned file size.

### Default Style

- Axis titles: Arial, bold, 24-28 pt.
- Tick labels: Arial, bold, 18-22 pt.
- Legend: Arial, 18-20 pt.
- Lines: 2 pt.
- Symbols: size 8-10, distinct shapes.
- Ticks: inward with minor ticks.
- Frame: four-sided closed frame.
- Grid: off.
- Background: white.

### Color Order

Use a colorblind-aware order:

1. blue
2. red
3. green
4. orange
5. purple
6. cyan

Avoid using red and green as the only two colors.

### Export Rule

Use `export_graph`. A successful export must report a generated file path and a non-trivial file size. If export fails, inspect the returned message and check whether Origin has a blocking dialog.

## 中文

当用户要求制作论文级 Origin Pro 图时，使用本工作流。

### 开始前确认

确认：

- 数据来源：直接数组、CSV 文件或已有 Origin 工作簿
- 图类型：scatter、line、line+symbol、bar、histogram 或其他
- 数据组数量
- 坐标轴名称和单位
- 目标期刊或样式偏好
- 导出目录和文件格式

如果用户没有指定样式，默认使用清爽论文图风格：Arial 字体、加粗坐标轴标题、向内刻度、四边框、无网格线、白底、兼顾色盲友好的配色。

### 推荐工具流程

1. 使用 `create_worksheet` 和 `set_worksheet_data`，或使用 `import_csv_to_worksheet`。
2. 使用 `create_graph`。
3. 多组数据时使用 `add_plot_to_graph`。
4. 使用 `apply_publication_style`。
5. 需要拟合时使用 `curve_fit`。
6. 使用 `export_graph` 导出，并检查返回的文件大小。

### 默认样式

- 坐标轴标题：Arial，加粗，24-28 pt。
- 刻度标签：Arial，加粗，18-22 pt。
- 图例：Arial，18-20 pt。
- 线宽：2 pt。
- 符号：大小 8-10，不同数据组使用不同形状。
- 刻度：向内，显示次刻度。
- 边框：四边闭合。
- 网格线：关闭。
- 背景：白色。

### 配色顺序

建议使用兼顾色盲友好的顺序：

1. blue
2. red
3. green
4. orange
5. purple
6. cyan

不要把红色和绿色作为仅有的两种颜色。

### 导出规则

使用 `export_graph`。只有当工具返回已生成文件路径并给出合理文件大小时，才视为导出成功。如果导出失败，先查看返回信息，并检查 Origin 是否有阻塞弹窗。
