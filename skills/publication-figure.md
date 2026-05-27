# Materials and Photodetector Publication Figure Workflow

Use this workflow when the user asks Origin Pro MCP to make publication-quality figures for materials characterization, optoelectronic devices, or general scientific datasets.

This file is intentionally domain-aware but not locked to one project. Use the general materials sections for any material system, and use the photodetector sections for detector metrics across different device stacks.

## Core Principle

Every figure should connect raw data to a physical evidence chain:

1. Goal: what the figure proves, compares, or screens.
2. Operation steps: cleaning, derived values, Origin tool flow, fitting, and export.
3. Expected result: what a healthy sample or device should show.
4. Failure criterion: what makes the plot misleading, under-calibrated, or physically suspicious.
5. Next step: the experiment, process action, or characterization implied by the plot.

For photodetectors, interpret every result through four dimensions:

- Band Alignment: junction energetics, contact selectivity, extraction barriers.
- Carrier Dynamics: photogeneration, transit, recombination, response speed.
- Trap States: leakage, hysteresis, persistent photoconductivity, slow tails.
- Built-in Field: rectification, zero-bias photovoltaic response, reverse-bias enhancement.

## Origin Tool Pattern

Use short ASCII-only Origin page names. Origin can truncate long workbook short names, which makes later `data_book` references miss the intended worksheet. Prefer names such as `RawData`, `Tauc`, `XRD`, `Raman`, `PL`, `XPS`, `AFM`, `Hall`, `IVSemi`, `Rectif`, `SpecMet`, `Noise`, `RespT`, `PowDep`, `Stats`, `FFTProf`, and `Orient`.

Default tool flow:

1. Confirm Origin Pro is running.
2. Ask before `new_project` if unsaved Origin work may exist.
3. Use `create_worksheet` and `set_worksheet_data`, or `import_csv_to_worksheet`.
4. Use `create_graph`.
5. Use `add_plot_to_graph` for additional datasets.
6. Use `apply_publication_style`.
7. Use `set_axis_range`, `set_plot_style`, `set_legend`, `set_tick_style`, or `run_labtalk` only for necessary refinements.
8. Use `curve_fit` when the model and fit range are physically justified.
9. Use `export_graph` and verify the returned file path and non-trivial file size.

## Metadata Before Final Figures

Ask for missing metadata before making a final figure:

- Sample name, stack, composition, treatment, and batch.
- Measurement date, atmosphere, temperature, instrument, and calibration state.
- Axis units and whether values are raw, normalized, offset, background-subtracted, or log-transformed.
- Film thickness for absorption coefficient or Tauc analysis.
- Active area for current density, responsivity, and detectivity.
- Bias convention, sweep direction, sweep rate, and whether current is `I` or current density `J`.
- Wavelength, optical power, power density, spot size, chopping frequency, and sampling rate for photodetectors.
- Noise definition for D*: measured spectral noise, RMS bandwidth-limited noise, or shot-noise estimate.
- Phase references for XRD, peak positions for Raman/PL, binding-energy calibration for XPS, and FFT calibration for TEM.

If data are incomplete, make an exploratory figure labelled as screening-level evidence and do not overclaim metrics.

## General Journal Style

Default style:

- Font: Arial.
- Axis title: 24-28 pt, bold.
- Tick label: 18-22 pt, bold.
- Legend: 16-20 pt.
- Line width: 2.0-2.5 pt.
- Symbol size: 8-10.
- Frame: four-sided closed frame.
- Ticks: inward, minor ticks visible.
- Grid: off.
- Background: white.
- Colors: blue, red, green, orange, purple, cyan.

Avoid red and green as the only pair. For spectra with many traces, use a restrained sequential palette plus clear offsets.

## Data Handling Rules

- Keep raw columns in the worksheet whenever possible.
- Compute derived values outside Origin when formulas must be auditable.
- State all floors used for log transforms, for example `max(abs(I), 1e-12 A)`.
- Do not smooth peak data aggressively. If smoothing is used, report the method and keep raw data available.
- Do not fit a full spectrum when only the edge or peak region is physically meaningful.
- Do not mix measured-noise and estimated-noise metrics on the same axis without clear labels.

## Template 1: Generic Multi-Dataset Figure

### Goal

Create a clean comparison figure for any x-y dataset, such as temperature-dependent intensity, time series, calibration curves, or normalized spectra.

### Operation Steps

```python
create_worksheet(book_name="RawData")
set_worksheet_data(
    book_name="RawData",
    sheet_name="Sheet1",
    columns="[x, y_sample_1, y_sample_2]",
    column_names="X,Sample_1,Sample_2"
)
create_graph(graph_name="FigGen", data_book="RawData", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line+symbol")
add_plot_to_graph(graph_name="FigGen", data_book="RawData", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line+symbol")
apply_publication_style(
    graph_name="FigGen",
    x_label="X label (unit)",
    y_label="Y label (unit)",
    legend_entries="Sample 1,Sample 2",
    legend_position="top-right"
)
```

### Expected Result

Datasets should be visually comparable without hiding absolute units or uncertainty.

### Failure Criterion

Axis labels lack units, normalization is not stated, or offsets make absolute values impossible to recover.

### Next Step

If trends are strong, add replicate statistics or fit a physically meaningful model. If trends are weak, verify calibration and sample identity first.

## Template 2: Tauc and Absorption Edge

### Goal

Extract optical bandgap or compare absorption edges for semiconductors, perovskites, quantum dots, thin films, or stacks.

### Operation Steps

Required data:

- `wavelength_nm` or photon energy.
- Absorbance, transmittance, or absorption coefficient.
- Film thickness when converting absorbance to absorption coefficient.
- Material assignment and Tauc exponent.

Derived values:

```text
hnu_eV = 1240 / wavelength_nm
alpha = 2.303 * Abs / thickness_cm
Tauc_y = (alpha * hnu_eV)^n
```

Common starting choices:

- Direct allowed transition: `n = 2`.
- Indirect allowed transition: `n = 0.5`.
- For quantum-confined systems, mixed phases, or multilayer stacks, state the literature assumption before choosing `n`.

Origin flow:

```python
create_worksheet(book_name="Tauc")
set_worksheet_data(
    book_name="Tauc",
    sheet_name="Sheet1",
    columns="[hnu_eV, Tauc_y]",
    column_names="Photon_energy,Tauc_y"
)
create_graph(graph_name="FigTauc", data_book="Tauc", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="scatter")
apply_publication_style(
    graph_name="FigTauc",
    x_label="Photon energy (eV)",
    y_label="(alpha hnu)^n",
    legend_entries="Tauc",
    legend_position="top-left"
)
```

### Expected Result

The linear edge region should be narrow, visually defensible, and consistent with the material system.

### Failure Criterion

Thickness is missing but `alpha` is claimed, the full spectrum is fit, or a stack spectrum is assigned to one layer without supporting evidence.

### Next Step

Use extracted bandgaps with UPS/KPFM/literature electron affinity values to support a band-alignment diagram.

## Template 3: XRD, Texture, and Phase Evidence

### Goal

Support phase identification, crystallinity, preferred orientation, and epitaxy-related claims.

### Operation Steps

Required data:

- `two_theta_deg`, intensity counts.
- Sample labels and substrate/reference traces.
- Radiation source and phase reference peaks.

Derived values:

```text
I_norm = intensity / max(intensity)
I_offset = I_norm + offset_per_sample
```

Origin flow:

```python
create_worksheet(book_name="XRD")
set_worksheet_data(
    book_name="XRD",
    sheet_name="Sheet1",
    columns="[two_theta, sample_1_offset, sample_2_offset, substrate_offset]",
    column_names="2theta,Sample_1,Sample_2,Substrate"
)
create_graph(graph_name="FigXRD", data_book="XRD", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
add_plot_to_graph(graph_name="FigXRD", data_book="XRD", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line")
add_plot_to_graph(graph_name="FigXRD", data_book="XRD", data_sheet="Sheet1", x_col=1, y_col=4, plot_type="line")
apply_publication_style(
    graph_name="FigXRD",
    x_label="2theta (degree)",
    y_label="Intensity (a.u.)",
    legend_entries="Sample 1,Sample 2,Substrate",
    legend_position="top-right"
)
```

### Expected Result

Peaks should match phase references, substrate peaks should be identified, and orientation claims should be supported by texture, phi-scan, or TEM FFT evidence.

### Failure Criterion

Epitaxy is claimed from out-of-plane XRD alone, substrate peaks are ignored, or peak shifts are discussed without calibration.

### Next Step

For reviewer-facing epitaxy evidence, add phi-scan, HRTEM-FFT orientation mapping, and interface continuity statistics.

## Template 4: Raman, PL, XPS, and UPS Spectra

### Goal

Compare vibrational, optical emission, chemical-state, or energy-level evidence across materials and treatments.

### Operation Steps

Raman/PL required data:

- `x`: Raman shift in cm^-1 or wavelength/energy.
- Intensity with background treatment stated.
- Peak assignments and measurement power if laser heating is possible.

XPS/UPS required data:

- Binding energy or kinetic energy axis.
- Raw and background-subtracted signal if available.
- Charge reference, typically C 1s = 284.8 eV for XPS when appropriate.

Origin flow:

```python
create_worksheet(book_name="Spec")
set_worksheet_data(
    book_name="Spec",
    sheet_name="Sheet1",
    columns="[x_axis, sample_1_offset, sample_2_offset]",
    column_names="X,Sample_1,Sample_2"
)
create_graph(graph_name="FigSpec", data_book="Spec", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
add_plot_to_graph(graph_name="FigSpec", data_book="Spec", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line")
apply_publication_style(
    graph_name="FigSpec",
    x_label="Raman shift (cm^-1)",
    y_label="Intensity (a.u.)",
    legend_entries="Sample 1,Sample 2",
    legend_position="top-right"
)
```

### Expected Result

Peak shifts, widths, intensity ratios, and binding-energy changes should support the stated phase, defect, composition, or energy-level claim.

### Failure Criterion

Background subtraction is hidden, charge correction is missing for XPS, PL is normalized in a way that hides quenching, or Raman laser power is not reported when heating is plausible.

### Next Step

Use peak fitting only after confirming the physical peak model, then connect chemical/defect evidence to transport, recombination, or detector noise.

## Template 5: SEM, TEM, FFT, and AFM Statistics

### Goal

Turn microscopy results into quantitative evidence for morphology, interface continuity, roughness, texture, grain size, defect density, or epitaxy.

### Operation Steps

Origin should plot derived microscopy data, not replace raw images:

- Grain-size histogram.
- AFM height or roughness distribution.
- Interface roughness profile.
- Defect density by type.
- FFT radial profile: `g_nm_inv` vs intensity.
- Azimuthal intensity: `phi_deg` vs intensity.

FFT radial profile:

```python
create_worksheet(book_name="FFTProf")
set_worksheet_data(
    book_name="FFTProf",
    sheet_name="Sheet1",
    columns="[g_nm_inv, intensity]",
    column_names="g,Intensity"
)
create_graph(graph_name="FigFFT", data_book="FFTProf", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
apply_publication_style(
    graph_name="FigFFT",
    x_label="Spatial frequency (nm^-1)",
    y_label="Intensity (a.u.)",
    legend_entries="FFT radial profile",
    legend_position="top-right"
)
```

Orientation or phi profile:

```python
create_worksheet(book_name="Orient")
set_worksheet_data(
    book_name="Orient",
    sheet_name="Sheet1",
    columns="[phi_deg, intensity_layer_1, intensity_layer_2]",
    column_names="Phi,Layer_1,Layer_2"
)
create_graph(graph_name="FigPhi", data_book="Orient", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
add_plot_to_graph(graph_name="FigPhi", data_book="Orient", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line")
apply_publication_style(
    graph_name="FigPhi",
    x_label="Azimuth angle (degree)",
    y_label="Intensity (a.u.)",
    legend_entries="Layer 1,Layer 2",
    legend_position="top-right"
)
```

### Expected Result

Quantitative plots should support what the images visually suggest: uniform coverage, lower roughness, larger grains, fewer pinholes, or reproducible orientation relationship.

### Failure Criterion

Only one local TEM image is used for global claims, FFT calibration is missing, or morphology evidence is not connected to device metrics.

### Next Step

Map morphology and structure metrics to leakage, rectification, response speed, responsivity, and D*.

## Template 6: Hall, Mobility, and Transport

### Goal

Summarize carrier type, carrier concentration, mobility, resistivity, and temperature-dependent transport.

### Operation Steps

Required data depends on the experiment:

- Hall: magnetic field, Hall voltage, current, thickness, geometry.
- Mobility: carrier density and conductivity or sheet resistance.
- Temperature transport: temperature and conductivity/resistivity.

Example flow:

```python
create_worksheet(book_name="Hall")
set_worksheet_data(
    book_name="Hall",
    sheet_name="Sheet1",
    columns="[temperature_K, mobility, carrier_density]",
    column_names="Temperature,Mobility,Carrier_density"
)
create_graph(graph_name="FigMob", data_book="Hall", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line+symbol")
apply_publication_style(
    graph_name="FigMob",
    x_label="Temperature (K)",
    y_label="Mobility (cm^2 V^-1 s^-1)",
    legend_entries="Mobility",
    legend_position="top-right"
)
```

### Expected Result

Trends should be consistent with the proposed transport mechanism and the device polarity or junction model.

### Failure Criterion

Geometry, thickness, or sign convention is missing, or mobility is calculated from mixed sheet and bulk units.

### Next Step

Use transport data to constrain band-alignment assumptions and contact-selectivity claims.

## Template 7: Photodetector I-V and Rectification

### Goal

Show leakage, rectification, dark/light separation, and bias-dependent operating behavior.

### Operation Steps

Required data:

- `V`: voltage in V.
- `I_dark`/`J_dark` and `I_light`/`J_light`.
- Active area if converting current to current density.
- Bias convention, sweep direction, illumination wavelength, optical power, and sweep rate.

Derived values:

```text
J = I / A_cm2
abs_J_dark = abs(J_dark)
abs_J_light = abs(J_light)
log_abs_J_dark = log10(max(abs_J_dark, floor))
log_abs_J_light = log10(max(abs_J_light, floor))
J_ph = J_light - J_dark
```

Origin flow:

```python
create_worksheet(book_name="IVSemi")
set_worksheet_data(
    book_name="IVSemi",
    sheet_name="Sheet1",
    columns="[V, log_abs_J_dark, log_abs_J_light]",
    column_names="Voltage,log10_abs_J_dark,log10_abs_J_light"
)
create_graph(graph_name="FigIV", data_book="IVSemi", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
add_plot_to_graph(graph_name="FigIV", data_book="IVSemi", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line")
apply_publication_style(
    graph_name="FigIV",
    x_label="Voltage (V)",
    y_label="log10(|J|) (mA cm^-2)",
    legend_entries="Dark,Light",
    legend_position="top-left"
)
```

Rectification:

```text
RR(V) = |J(+V)| / max(|J(-V)|, floor)
log_RR = log10(RR)
```

### Expected Result

Dark current should remain low in the intended reverse-bias region, and illuminated current should separate clearly from dark current.

### Failure Criterion

Negative or zero current is plotted directly on a log axis, current/current-density units are mixed, or hysteresis is hidden by combining mismatched sweep directions.

### Next Step

If leakage is high, prioritize SEM pinholes, TEM grain boundaries/dislocations, surface roughness, contact shunts, and sputter/ALD damage checks.

## Template 8: EQE, Responsivity, and Detectivity

### Goal

Show spectral photodetection performance and separate optical absorption effects from electrical noise limits.

### Operation Steps

Required data:

- `lambda_nm`: wavelength in nm.
- `P_lambda`: optical power in W, or power density in W cm^-2.
- `I_light`, `I_dark`: current in A.
- `A_cm2`: active area.
- `i_noise`: noise current in A Hz^-1/2 if measured.

Derived values:

```text
I_ph = I_light - I_dark
P_total = power_density * A_cm2
R = I_ph / P_lambda
EQE = R * 1240 / lambda_nm
Dstar = R * sqrt(A_cm2) / i_noise
log_Dstar = log10(Dstar)
```

If noise is not measured, label D* as estimated and state the noise model.

Origin flow:

```python
create_worksheet(book_name="SpecMet")
set_worksheet_data(
    book_name="SpecMet",
    sheet_name="Sheet1",
    columns="[lambda_nm, EQE_percent, R_A_per_W, log_Dstar]",
    column_names="Wavelength,EQE,Responsivity,log10_Dstar"
)
create_graph(graph_name="FigEQE", data_book="SpecMet", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line+symbol")
apply_publication_style(graph_name="FigEQE", x_label="Wavelength (nm)", y_label="EQE (%)", legend_entries="EQE", legend_position="top-right")
create_graph(graph_name="FigR", data_book="SpecMet", data_sheet="Sheet1", x_col=1, y_col=3, plot_type="line+symbol")
apply_publication_style(graph_name="FigR", x_label="Wavelength (nm)", y_label="Responsivity (A W^-1)", legend_entries="R", legend_position="top-right")
create_graph(graph_name="FigDstar", data_book="SpecMet", data_sheet="Sheet1", x_col=1, y_col=4, plot_type="line+symbol")
apply_publication_style(graph_name="FigDstar", x_label="Wavelength (nm)", y_label="log10(D*) (Jones)", legend_entries="D*", legend_position="top-right")
```

### Expected Result

Spectral response should follow absorption features and detector selectivity. D* should reflect both high responsivity and low noise, not only large photocurrent.

### Failure Criterion

Active area, power calibration, or noise definition is missing; EQE exceeds plausible values without gain discussion; measured and estimated D* are mixed.

### Next Step

If D* is low despite high responsivity, prioritize noise spectrum, dark-current suppression, trap passivation, and contact optimization.

## Template 9: Noise Spectrum and NEP

### Goal

Quantify the noise floor that limits D*, detect low-frequency trap noise, and separate shot, thermal, and 1/f components.

### Operation Steps

Required data:

- Frequency in Hz.
- Current noise density in A Hz^-1/2.
- Bias, dark/light condition, bandwidth, and preamplifier settings.

Derived values:

```text
NEP = i_noise / R
Dstar = sqrt(A_cm2) / NEP
```

Origin flow:

```python
create_worksheet(book_name="Noise")
set_worksheet_data(
    book_name="Noise",
    sheet_name="Sheet1",
    columns="[freq_Hz, log_i_noise]",
    column_names="Frequency,log10_i_noise"
)
create_graph(graph_name="FigNoise", data_book="Noise", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
apply_publication_style(
    graph_name="FigNoise",
    x_label="Frequency (Hz)",
    y_label="log10(i_n) (A Hz^-1/2)",
    legend_entries="Noise",
    legend_position="top-right"
)
```

### Expected Result

Low-frequency noise should be visible if trap states or photogating dominate. A flatter spectrum supports white-noise-limited operation.

### Failure Criterion

Bandwidth, gain, or instrument floor is missing, or D* is calculated from noise measured under mismatched bias/illumination.

### Next Step

Compare noise trends with dark current, trap-state signatures, and response-time tails.

## Template 10: Response Time

### Goal

Quantify carrier dynamics, trap-related slow tails, and photogating behavior.

### Operation Steps

Required data:

- `time_s`, current/current density.
- Light on/off markers or chopping period.
- Bias, wavelength, optical power, sampling rate.

Derived values:

```text
I_norm = (I_t - I_dark) / (I_light_steady - I_dark)
rise_time = t90_on - t10_on
fall_time = t10_off - t90_off
```

Origin flow:

```python
create_worksheet(book_name="RespT")
set_worksheet_data(
    book_name="RespT",
    sheet_name="Sheet1",
    columns="[time_s, I_norm]",
    column_names="Time,I_norm"
)
create_graph(graph_name="FigResp", data_book="RespT", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="line")
apply_publication_style(
    graph_name="FigResp",
    x_label="Time (s)",
    y_label="Normalized photocurrent",
    legend_entries="Response",
    legend_position="bottom-right"
)
```

### Expected Result

Fast rise/fall indicates efficient separation and extraction. Slow decay suggests trap states, interfacial barriers, or photogating.

### Failure Criterion

Sampling interval is too coarse, baseline drift is not corrected, or rise/fall definition is not reported.

### Next Step

If response is slow, perform light-intensity dependence, trap-state analysis, passivation tests, and interface/barrier tuning.

## Template 11: Light-Intensity Dependence

### Goal

Diagnose recombination, traps, photogating, and gain through photocurrent scaling with optical power.

### Operation Steps

Required data:

- Optical power or power density.
- Photocurrent under fixed bias and wavelength.
- Dark current and active area.

Derived values:

```text
I_ph = I_light - I_dark
log_Iph = log10(max(I_ph, floor))
log_P = log10(P)
Fit: I_ph = a * P^theta
```

Origin flow:

```python
create_worksheet(book_name="PowDep")
set_worksheet_data(
    book_name="PowDep",
    sheet_name="Sheet1",
    columns="[log_P, log_Iph]",
    column_names="log10_P,log10_Iph"
)
create_graph(graph_name="FigPow", data_book="PowDep", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="scatter")
apply_publication_style(
    graph_name="FigPow",
    x_label="log10(P) (W)",
    y_label="log10(I_ph) (A)",
    legend_entries="Power law",
    legend_position="top-left"
)
```

### Expected Result

`theta` close to 1 suggests near-linear response. Sublinear behavior suggests traps, recombination, space-charge effects, or saturation.

### Failure Criterion

Power calibration is missing, dark current is not subtracted, or the fit includes saturated points without discussion.

### Next Step

If sublinear, compare with response-time tails and noise spectra to identify trap-assisted photogating.

## Template 12: Device Statistics

### Goal

Report reproducibility across devices, batches, treatments, or process windows.

### Operation Steps

Recommended metrics:

- Dark current density at a fixed bias.
- Responsivity at a fixed wavelength and bias.
- D* at a fixed wavelength and bias.
- Rise/fall time.
- Rectification ratio.
- Yield or failure count.

Origin flow:

```python
create_worksheet(book_name="Stats")
set_worksheet_data(
    book_name="Stats",
    sheet_name="Sheet1",
    columns="[device_index, dark_J, R, log_Dstar]",
    column_names="Device,Dark_J,Responsivity,log10_Dstar"
)
create_graph(graph_name="FigStats", data_book="Stats", data_sheet="Sheet1", x_col=1, y_col=2, plot_type="scatter")
apply_publication_style(
    graph_name="FigStats",
    x_label="Device index",
    y_label="Dark current density (mA cm^-2)",
    legend_entries="Devices",
    legend_position="top-right"
)
```

### Expected Result

Statistics should show whether the reported best device is representative or an outlier.

### Failure Criterion

Only the best device is shown, failed devices are excluded without reporting yield, or measurement conditions differ across devices.

### Next Step

Use distributions to choose the next process experiment: pinhole reduction, interface passivation, thickness optimization, or contact protection.

## Manuscript Figure Set Recommendation

For a materials photodetector paper, build figures in this order:

1. Material/device stack and band alignment.
2. Structure and morphology: XRD, Raman/PL/XPS as relevant, SEM/TEM/AFM statistics.
3. Junction behavior: I-V semilog, rectification, dark/light current.
4. Spectral performance: EQE, responsivity, D*, absorption/Tauc support.
5. Dynamics and noise: response time, noise spectrum, light-intensity dependence.
6. Reproducibility: device statistics and yield.
7. Mechanism figure: connect structure and traps to performance metrics.

## Reporting Checklist

Before final export, verify:

- [ ] Axis labels include units.
- [ ] Normalization, offsets, smoothing, and log floors are stated.
- [ ] Fit model and fit range are stated.
- [ ] Film thickness is included for absorption coefficient or Tauc analysis.
- [ ] XRD phase references and substrate peaks are labeled.
- [ ] Raman/PL peak assignments or XPS charge references are reported when relevant.
- [ ] TEM/FFT calibration and sampled regions are stated.
- [ ] Active area is included for current density, R, EQE, and D*.
- [ ] Bias, wavelength, optical power, and atmosphere/temperature are reported.
- [ ] Noise definition is reported for D*.
- [ ] Rise/fall time definition and sampling interval are reported.
- [ ] Structure plots are tied to device metrics.
- [ ] Exported files exist and have non-trivial size.

## 中文速查

本工作流用于 Origin Pro 论文图自动化，覆盖通用材料表征和光电探测器指标图。制作最终图时，每张图都要给出目标、操作步骤、预期结果、失败判据和下一步。

通用材料优先覆盖：

- Tauc/吸收边：必须说明膜厚、Tauc 指数、线性拟合区间。
- XRD/取向：必须标注相参考、衬底峰；不能只靠 out-of-plane XRD 声称外延。
- Raman/PL/XPS/UPS：必须说明背景、归一化、峰归属和能量校准。
- SEM/TEM/FFT/AFM：必须把形貌转化为统计量，并对应到器件漏电、整流、响应速度或 D*。
- Hall/迁移率：必须说明厚度、几何、符号约定和单位。

光电探测器优先覆盖：

- I-V 和整流比：明确电压符号、扫描方向、电流/电流密度、正反偏定义，并按用户给定器件结构解释。
- EQE、响应度、D*：明确活性面积、光功率、噪声定义；未测噪声时只能写 estimated D*。
- 噪声谱和 NEP：说明带宽、增益、仪器噪声底和测试偏压。
- 响应时间：说明采样间隔、rise/fall 定义和光开关条件。
- 光强依赖：用 `I_ph = a * P^theta` 判断线性、陷阱和光生门控。
