# Materials and Photodetector Extension Notes

中文见下半部分。

## English

### Branch Purpose

This branch turns `origin-pro-mcp-skill` from a general Origin Pro automation skill into a broader scientific plotting package for materials characterization and photodetector data analysis.

The package remains device-agnostic. It does not assume a specific material system, layer stack, polarity convention, or detector architecture.

### Skill Package Details

The enhanced skill helps an AI assistant use Origin Pro to:

- Import or write raw numeric data into Origin worksheets.
- Build publication-quality graphs with verified export.
- Preserve raw and derived columns for auditable scientific figures.
- Apply consistent journal-style formatting through `apply_publication_style`.
- Use Origin fitting only when the model and fit range are physically justified.
- Report the metadata needed for materials and optoelectronic device figures.

### Materials Figure Coverage

The workflow now includes templates and reporting rules for:

- Absorption and Tauc bandgap plots.
- XRD phase, texture, and orientation evidence.
- Raman, PL, XPS, and UPS spectra.
- SEM, TEM, FFT, and AFM derived statistics.
- Hall, mobility, carrier density, and transport plots.

### Photodetector Figure Coverage

The workflow now includes templates and reporting rules for:

- I-V semilog and rectification plots.
- Photocurrent extraction.
- EQE, responsivity, D*, and NEP.
- Measured or estimated noise spectra.
- Response-time traces and rise/fall definitions.
- Light-intensity dependence and power-law fitting.
- Cross-device statistics and reproducibility plots.

### Updates Compared with the Original Version

- Expanded `SKILL.md` trigger text from general Origin plotting to materials characterization and photodetector metrics.
- Replaced the compact `skills/publication-figure.md` with a detailed reusable workflow containing 12 figure templates.
- Added explicit rules for metadata, derived-value calculation, fit-range reporting, log-transform floors, and export validation.
- Added photodetector interpretation dimensions: band alignment, carrier dynamics, trap states, and built-in field.
- Updated `README.md` and `README.zh-CN.md` with materials and photodetector workflow summaries.
- Updated `agents/openai.yaml` so UI surfaces advertise the new materials and photodetector capability.
- Bumped the package version to `0.2.2` and added related package keywords.

## 中文

### 分支目的

本分支将 `origin-pro-mcp-skill` 从通用 Origin Pro 自动化技能，扩展为面向材料表征和光电探测器数据分析的科研绘图技能包。

该版本保持通用性，不预设特定材料体系、器件结构、极性约定或探测器架构。

### 技能包详情

增强后的技能可帮助 AI 助手使用 Origin Pro 完成：

- 导入或写入原始数值数据到 Origin 工作表。
- 创建论文级图像并校验导出文件。
- 同时保留原始列和派生列，方便科研图溯源。
- 通过 `apply_publication_style` 应用统一论文图样式。
- 仅在模型和拟合区间物理合理时使用 Origin 拟合。
- 为材料和光电子器件图补齐必要测试元数据。

### 材料表征图覆盖范围

当前工作流加入了以下模板和汇报规则：

- 吸收与 Tauc 带隙图。
- XRD 物相、织构和取向证据图。
- Raman、PL、XPS、UPS 光谱图。
- SEM、TEM、FFT、AFM 的派生统计图。
- Hall、迁移率、载流子浓度和输运图。

### 光电探测器图覆盖范围

当前工作流加入了以下模板和汇报规则：

- I-V 半对数图和整流比图。
- 光电流提取。
- EQE、响应度、D* 和 NEP。
- 实测或估算噪声谱。
- 响应时间曲线与 rise/fall 定义。
- 光强依赖和幂律拟合。
- 跨器件统计与可重复性图。

### 相较于原版的更新

- 将 `SKILL.md` 的触发说明从通用 Origin 绘图扩展到材料表征和光电探测器指标。
- 将简版 `skills/publication-figure.md` 升级为包含 12 类图模板的可复用工作流。
- 增加元数据、派生值计算、拟合区间、log 变换 floor 和导出校验规则。
- 增加光电探测器解释维度：band alignment、carrier dynamics、trap states、built-in field。
- 在 `README.md` 和 `README.zh-CN.md` 中同步材料和光电探测器工作流说明。
- 更新 `agents/openai.yaml`，让 UI 入口能够展示新的材料和光电探测器能力。
- 将包版本提升到 `0.2.2`，并补充相关关键词。
