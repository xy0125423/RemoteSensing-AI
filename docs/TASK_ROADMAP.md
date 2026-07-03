# TASK_ROADMAP — 任务路线图

> ⚠️ **这是最重要的文档。**  
> 未来六个月，你每天只需要打开这个文件，完成当天的一个 Task 即可。  
> 每个 Task 都可以独立发给任何 AI 辅助完成。

---

## 使用说明

1. 按顺序执行，每个 Task 的「依赖任务」必须全部完成才能开始
2. 每完成一个 Task，在 `[ ]` 中打 `[x]`，在 TODAY.md 中记录
3. 每个 Task 设计为 1~3 小时，正好是你一天的投入量
4. 如果一个 Task 超过 3 小时还没完成 → 拆分，记录到 NOTES.md

---

## Phase 1：GeoTIFF 驯服战（Task 01 ~ 07）

---

### [x] Task 01：从 GEE 导出第一张 Sentinel-2 GeoTIFF 到 Google Drive ✅ 2026-07-03

- **Phase**：Phase 1
- **预计耗时**：2 小时
- **依赖任务**：Phase 0 完成
- **任务描述**：
  在 GEE Code Editor 中，使用 Export.image.toDrive() 将 Phase 0 筛选出的 28 景影像中的第一景导出到 Google Drive。设置 scale=10（10米分辨率），只导出 B4、B3、B2、B8 四个波段。
- **具体动作**：
  1. 在 GEE 中取 `collection.first()` 获得第一景影像
  2. 使用 `.select(['B4', 'B3', 'B2', 'B8'])` 选波段
  3. 调用 `Export.image.toDrive()` 设置参数
  4. 在 Tasks 面板点击 Run
  5. 等待导出完成，在 Google Drive 确认文件存在
- **完成标志**：
  - Google Drive 中出现一个 `.tif` 文件
  - 文件大小约 50~200 MB
- **常见坑**：导出区域太大会导致文件过大、导出超时。建议先用小区域测试。

---

### [x] Task 02：从 Google Drive 下载 GeoTIFF 到本地 data/raw/ ✅ 2026-07-03

- **Phase**：Phase 1
- **预计耗时**：1 小时
- **依赖任务**：Task 01
- **任务描述**：
  从 Google Drive 手动下载 Task 01 导出的 GeoTIFF 文件，放到项目的 `data/raw/` 目录，文件命名为 `sentinel2_first.tif`。
- **具体动作**：
  1. 打开 Google Drive，找到导出的 tif 文件
  2. 下载到 `data/raw/`
  3. 在 VS Code 中确认文件存在
  4. 在 `.gitignore` 中确认 `data/raw/` 不被 Git 追踪
- **完成标志**：
  - `data/raw/sentinel2_first.tif` 存在
  - 文件大小与 Google Drive 一致
- **常见坑**：Google Drive 下载大文件可能断连，用浏览器直接下载比用 API 更可靠。

---

### Task 03：使用 rasterio 读取 GeoTIFF 并打印全部元数据

- **Phase**：Phase 1
- **预计耗时**：2 小时
- **依赖任务**：Task 02
- **任务描述**：
  编写 Python 脚本 `src/read_geotiff.py`，使用 rasterio 打开 Task 02 下载的 GeoTIFF，打印所有元数据：CRS、Transform、Bounds、Width、Height、波段数、数据类型。
- **具体动作**：
  1. `import rasterio`
  2. `with rasterio.open('data/raw/sentinel2_first.tif') as src:`
  3. 打印 `src.crs`、`src.transform`、`src.bounds`、`src.width`、`src.height`、`src.count`、`src.dtypes`
  4. 打印每个波段的描述（`src.descriptions`）
  5. 运行脚本，截图保存输出
- **完成标志**：
  - 终端输出完整的 GeoTIFF 元数据
  - 能说出：这张影像的坐标系是什么、分辨率是多少、有几个波段
- **常见坑**：rasterio 需要系统有 GDAL，Windows 上建议用 `pip install rasterio` 的 wheel 包。如果报 DLL 错误，参考 RISK.md。

---

### Task 04：提取 B4 和 B8 波段为 numpy 数组并打印统计信息

- **Phase**：Phase 1
- **预计耗时**：2 小时
- **依赖任务**：Task 03
- **任务描述**：
  扩展 `src/read_geotiff.py`，读取 B4（Red）和 B8（NIR）波段的数据为 numpy 数组。打印每个波段的最小值、最大值、均值、标准差。注意 Sentinel-2 数据可能是 uint16 类型。
- **具体动作**：
  1. 使用 `src.read(band_index)` 读取单个波段（注意 rasterio 的 band index 从 1 开始）
  2. 将数据转为 `float32` 或 `float64`
  3. 使用 `numpy` 计算 min、max、mean、std
  4. 打印结果
- **完成标志**：
  - 终端输出 B4 和 B8 的 min、max、mean、std
  - 数值在合理范围内（反射率 × 10000，通常在 0~10000）
- **常见坑**：波段索引从 1 开始不是 0。注意 Sentinel-2 L2A 产品数据已经是地表反射率（缩放 10000）。

---

### Task 05：使用 matplotlib 显示 Sentinel-2 真彩色影像（B4-B3-B2）

- **Phase**：Phase 1
- **预计耗时**：3 小时
- **依赖任务**：Task 04
- **任务描述**：
  编写脚本 `src/display_rgb.py`，读取 B4、B3、B2 三个波段，使用 matplotlib 将其合成为真彩色影像并显示。要求：坐标轴显示经纬度、添加颜色条、添加标题。
- **具体动作**：
  1. 读取 B4(Red)、B3(Green)、B2(Blue) 三个波段
  2. 将三个波段 stack 为 (H, W, 3) 的 RGB 数组
  3. 对数据进行 2%~98% 拉伸（clip），增强对比度
  4. 使用 `plt.imshow()` 显示
  5. 尝试使用 rasterio 的 `src.transform` 来设置正确的坐标轴（或用 `extent` 参数简单处理）
- **完成标志**：
  - 弹出 matplotlib 窗口，显示一张看起来像航拍照片的真彩色影像
  - 图片颜色自然，不过曝、不过暗
- **常见坑**：uint16 数据直接显示会全白。必须先 clip 再 normalize 到 0~1。Sentinel-2 L2A 的反射率需要除以 10000。

---

### Task 06：编写批量导出脚本 — 从 GEE 导出全部 28 景影像

- **Phase**：Phase 1
- **预计耗时**：3 小时
- **依赖任务**：Task 01
- **任务描述**：
  在 GEE 中编写脚本，对 Phase 0 筛选出的 28 景影像，循环调用 Export.image.toDrive() 批量导出。每次导出时在文件名中包含日期信息。不使用 GEE Python API，直接在 Code Editor 中用 JavaScript 完成。
- **具体动作**：
  1. 获取筛选后的 ImageCollection
  2. 将其转为 List
  3. 使用 `map()` 或 `evaluate()` 遍历
  4. 每个影像导出为单独的 GeoTIFF，文件名如 `S2_20250315`
  5. 在 Tasks 面板确认 28 个任务都已创建
- **完成标志**：
  - GEE Tasks 面板中有 28 个导出任务
  - 至少 5 个任务状态变为 Completed
- **常见坑**：GEE 有并发导出限制，Tasks 太多会排队。不需要等 28 个全部完成才进入 Task 07，有 5 个就可以开始。

---

### Task 07：下载 5 景 GeoTIFF 到本地并批量读取元数据

- **Phase**：Phase 1
- **预计耗时**：2 小时
- **依赖任务**：Task 06
- **任务描述**：
  从 Google Drive 下载至少 5 景 GeoTIFF 到 `data/raw/`。编写脚本 `src/batch_read.py` 批量读取所有 GeoTIFF 的元数据，汇总为一张表格（日期、云量、波段数、文件大小）并打印。
- **具体动作**：
  1. 手动下载 5 景 GeoTIFF 到 `data/raw/`
  2. 使用 `glob` 找到所有 `.tif` 文件
  3. 遍历每个文件，用 rasterio 读取元数据
  4. 使用 pandas （可选）或直接 print 输出汇总表格
- **完成标志**：
  - `data/raw/` 中有 5 个 GeoTIFF 文件
  - 终端输出汇总表格
- **常见坑**：GEE 导出文件名可能包含特殊字符。统一命名规范很重要。

---

### ✅ Phase 1 检查点

- [ ] Task 01 ~ 07 全部完成
- [ ] 能独立完成：GEE 导出 → 本地 GeoTIFF → rasterio 读取 → matplotlib 显示
- [ ] `data/raw/` 中至少有 5 景影像

---

## Phase 2：NDVI 计算引擎（Task 08 ~ 14）

---

### Task 08：理解 NDVI 公式并手动计算一个像素的 NDVI

- **Phase**：Phase 2
- **预计耗时**：1.5 小时
- **依赖任务**：Task 04
- **任务描述**：
  不写完整的脚本。在 Python 交互环境中（或 Jupyter Notebook），手动选一个像素，用 B4 和 B8 的值计算 NDVI。验证公式：NDVI = (NIR - Red) / (NIR + Red)。确保结果在 -1 到 1 之间。
- **具体动作**：
  1. 读取 B4 和 B8 数组
  2. 取 [100, 100] 位置的像素值
  3. 手动计算 NDVI
  4. 对比 numpy 向量化计算的结果
  5. 理解 NDVI 为什么在 -1~1 之间
- **完成标志**：
  - 能口述 NDVI 公式
  - 能解释为什么 NDVI > 0.3 通常表示植被
- **常见坑**：分母为 0 会导致 NaN（水体）。需要处理除零问题。

---

### Task 09：编写 NDVI 计算函数并生成 NDVI 单景影像

- **Phase**：Phase 2
- **预计耗时**：2 小时
- **依赖任务**：Task 08
- **任务描述**：
  编写 `src/ndvi_calc.py`，包含函数 `calculate_ndvi(red_band, nir_band)`，输入两个 numpy 数组，返回 NDVI 数组。对一景影像计算 NDVI 并保存为 GeoTIFF。
- **具体动作**：
  1. 实现 `calculate_ndvi(red, nir)` 函数
  2. 处理除零：`np.where(red + nir == 0, 0, (nir - red) / (nir + red))`
  3. 使用 rasterio 的元数据将 NDVI 数组写回 GeoTIFF
  4. 保存到 `data/processed/ndvi_first.tif`
- **完成标志**：
  - `data/processed/ndvi_first.tif` 存在
  - 能用 rasterio 重新读取并验证 NDVI 值在 -1~1
- **常见坑**：数据类型转换。NDVI 是 float，写入 GeoTIFF 需要指定 dtype=float32。

---

### Task 10：生成 NDVI 伪彩色图

- **Phase**：Phase 2
- **预计耗时**：2 小时
- **依赖任务**：Task 09
- **任务描述**：
  扩展 `src/ndvi_calc.py` 或新写 `src/visualize_ndvi.py`，读取 NDVI GeoTIFF，使用 matplotlib 生成伪彩色图。绿色表示高 NDVI（植被），棕色/黄色表示低 NDVI（裸土/建筑），蓝色表示负 NDVI（水体）。
- **具体动作**：
  1. 使用 matplotlib 的 `imshow()` 显示 NDVI
  2. 选择合适的 colormap（推荐 RdYlGn 或 BrBG）
  3. 设置 vmin=-1, vmax=1
  4. 添加 colorbar
  5. 保存为 `outputs/ndvi_map.png`
- **完成标志**：
  - `outputs/ndvi_map.png` 存在
  - 图中绿色区域对应植被区，棕色对应裸土
- **常见坑**：colormap 选择不当会导致视觉效果差。建议用 RdYlGn（红-黄-绿）。

---

### Task 11：在 GEE 中直接计算 NDVI（云端方案对比）

- **Phase**：Phase 2
- **预计耗时**：3 小时
- **依赖任务**：Task 09
- **任务描述**：
  在 GEE Code Editor 中，对筛选的 28 景 Sentinel-2 影像，使用 `.map()` 在云端逐景计算 NDVI。对比云端计算和本地计算的结果差异。理解两种方案各自的适用场景。
- **具体动作**：
  1. 定义 NDVI 计算函数：`function(img) { return img.addBands(img.normalizedDifference(['B8', 'B4']).rename('NDVI')); }`
  2. 对 ImageCollection 执行 `.map(calcNDVI)`
  3. 对其中一景，导出 NDVI 波段到 Drive
  4. 下载后与 Task 09 的本地计算结果对比
- **完成标志**：
  - 能说出 GEE 云端计算 NDVI 和本地计算各自的优缺点
  - 两种方案的 NDVI 数值差异 < 0.001
- **常见坑**：GEE 的 `normalizedDifference()` 自动处理除零。云端计算更快但灵活性不如本地。

---

### Task 12：批量计算 28 景影像的 NDVI 均值并保存 CSV

- **Phase**：Phase 2
- **预计耗时**：3 小时
- **依赖任务**：Task 09, Task 06
- **任务描述**：
  对本地已有的每景 GeoTIFF，计算整景 NDVI 的均值（或仅计算植被区域均值），将结果保存为 CSV 文件：`data/processed/ndvi_series.csv`。每行包含：影像日期、NDVI 均值、NDVI 标准差、有效像素数。
- **具体动作**：
  1. 遍历 `data/raw/` 中所有 GeoTIFF
  2. 对每景计算 NDVI 均值
  3. 使用 Python 的 csv 模块或 pandas 写入 CSV
  4. CSV 列：date, ndvi_mean, ndvi_std, valid_pixels
- **完成标志**：
  - `data/processed/ndvi_series.csv` 存在
  - 至少有 5 行数据（5 个不同日期）
  - NDVI 均值在合理范围（0.1~0.8）
- **常见坑**：如果本地 GeoTIFF 不够 28 景，先用已有的做。云覆盖区域的 NDVI 可能异常，需要在后续处理。

---

### Task 13：在 GEE 中直接提取 NDVI 时间序列（云端方案对比）

- **Phase**：Phase 2
- **预计耗时**：2 小时
- **依赖任务**：Task 11
- **任务描述**：
  在 GEE Code Editor 中，使用 `ui.Chart.image.series()` 直接绘制研究区的 NDVI 时间序列折线图。这是 GEE 内置的时序可视化功能，不需要导出数据到本地。
- **具体动作**：
  1. 对 ImageCollection 计算 NDVI
  2. 使用 `ui.Chart.image.series()` 绘制 NDVI 均值时序图
  3. 观察折线图的大致形态（波峰、波谷、趋势）
  4. 截图保存到 `outputs/gee_ndvi_chart.png`
- **完成标志**：
  - GEE 中显示 NDVI 时间序列折线图
  - 能识别出植被生长的季节性波动
- **常见坑**：`ui.Chart.image.series()` 需要指定 reducer（如 `ee.Reducer.mean()`）和 geometry。

---

### Task 14：确定最终技术方案并写 DECISIONS 记录

- **Phase**：Phase 2
- **预计耗时**：1 小时
- **依赖任务**：Task 12, Task 13
- **任务描述**：
  对比"本地 NDVI 计算"和"GEE 云端 NDVI 计算"两种方案，做出最终选择并写入 `DECISIONS.md`。后续 Phase 3~6 将基于此决定进行。
- **具体动作**：
  1. 列出两种方案的优缺点
  2. 考虑因素：数据量、计算速度、灵活性、学习价值
  3. 做出决策并写入 DECISIONS.md
  4. 推荐方案：**GEE 计算 NDVI + 导出 NDVI 时间序列 CSV 到本地 + 本地做时序分析和 FFT**
- **完成标志**：
  - `DECISIONS.md` 中新增一条决策记录
  - 后续 Task 的技术路线明确
- **常见坑**：不要追求完美方案。GEE 计算 NDVI 最省事，本地做后续分析最能学到东西。

---

### ✅ Phase 2 检查点

- [ ] Task 08 ~ 14 全部完成
- [ ] 能手写 NDVI = (NIR - Red) / (NIR + Red)
- [ ] `data/processed/ndvi_series.csv` 存在且数据合理
- [ ] 技术方案决策已写入 DECISIONS.md

---

## Phase 3：时间序列分析（Task 15 ~ 20）

---

### Task 15：读取 ndvi_series.csv 并绘制原始 NDVI 时序折线图

- **Phase**：Phase 3
- **预计耗时**：2 小时
- **依赖任务**：Task 14
- **任务描述**：
  编写 `src/timeseries.py`，读取 `ndvi_series.csv`，使用 matplotlib 绘制 (日期, NDVI均值) 的散点图和折线图。横轴为日期，纵轴为 NDVI。这是最原始的 NDVI 时序可视化。
- **具体动作**：
  1. 使用 pandas 读取 CSV（或 csv 模块）
  2. 将日期列转为 datetime 类型
  3. 按日期排序
  4. 使用 `plt.plot()` 绘制折线图
  5. 使用 `plt.scatter()` 叠加散点（显示实际采样点）
  6. 保存为 `outputs/ndvi_timeseries_raw.png`
- **完成标志**：
  - `outputs/ndvi_timeseries_raw.png` 存在
  - 图中能看到 NDVI 随时间的变化模式
- **常见坑**：日期格式不一致。注意 Sentinel-2 的 5 天重访周期意味着采样点不均匀分布。

---

### Task 16：检测并处理 NDVI 异常值

- **Phase**：Phase 3
- **预计耗时**：2.5 小时
- **依赖任务**：Task 15
- **任务描述**：
  在 `src/timeseries.py` 中增加异常值检测功能。NDVI 序列中的异常值通常来自云漏检（NDVI 异常偏低）或阴影。使用统计方法（如偏离滑动中位数 2 倍 MAD）检测并标记异常点。在折线图中用红色高亮异常点。
- **具体动作**：
  1. 计算 NDVI 序列的滑动中位数（窗口=3）
  2. 计算 MAD（Median Absolute Deviation）
  3. 标记偏离中位数超过 2×MAD 的点为异常
  4. 在折线图中用红色 × 标记异常点
  5. 保存标注后的图
- **完成标志**：
  - 异常点被正确标记
  - 图中红色 × 对应明显偏离整体趋势的点
- **常见坑**：MAD 阈值设太严会误判正常波动。先可视化再手动确认。

---

### Task 17：对 NDVI 序列做线性插值，得到均匀时间步长

- **Phase**：Phase 3
- **预计耗时**：2.5 小时
- **依赖任务**：Task 16
- **任务描述**：
  Sentinel-2 重访周期约 5 天，但受云量过滤影响，实际采样点不均匀。使用 numpy.interp 或 pandas.interpolate 对 NDVI 序列做线性插值，得到每天一个值的均匀序列。这是后续 FFT 分析的必要前处理。
- **具体动作**：
  1. 创建均匀的日期序列（从最早日期到最晚日期，步长=1天）
  2. 使用 `np.interp()` 对 NDVI 值进行线性插值
  3. 绘制插值前后的对比图（原始散点 + 插值线）
  4. 保存插值后的数据为 `data/processed/ndvi_interpolated.csv`
- **完成标志**：
  - 插值后的序列每天一个 NDVI 值
  - 对比图中插值线穿过原始散点
  - FFT 的前置条件满足（均匀采样）
- **常见坑**：线性插值在长空白期（如冬季连续多云）会产生不合理的直线段。可以在后续 Task 使用更好的插值方法。

---

### Task 18：对 NDVI 序列做滑动平均平滑

- **Phase**：Phase 3
- **预计耗时**：2 小时
- **依赖任务**：Task 17
- **任务描述**：
  对插值后的 NDVI 序列应用滑动平均（Moving Average），窗口大小设为 15 天或 30 天。目的是滤除高频噪声（单次云阴影、大气校正误差），保留季节性的植被变化信号。绘制原始插值线与平滑线的对比图。
- **具体动作**：
  1. 使用 `np.convolve()` 或 `pandas.rolling().mean()` 实现滑动平均
  2. 测试不同窗口大小（7天、15天、30天）的效果
  3. 绘制对比图：原始（灰）vs 平滑（绿）
  4. 选择最合适的窗口大小并记录原因
- **完成标志**：
  - 平滑后曲线清晰显示植被的季节性变化
  - 对比图保存为 `outputs/ndvi_smoothed.png`
- **常见坑**：窗口太大 → 把真实的季节变化也平滑掉了。需要目视判断。

---

### Task 19：提取 NDVI 物候指标

- **Phase**：Phase 3
- **预计耗时**：3 小时
- **依赖任务**：Task 18
- **任务描述**：
  从平滑后的 NDVI 序列中提取关键物候指标：NDVI 最大值及对应日期（生长季峰值）、NDVI 最小值及对应日期、生长季振幅（最大值 - 最小值）、生长季起始日期（NDVI 首次超过阈值）、生长季结束日期（NDVI 首次低于阈值）。
- **具体动作**：
  1. 使用 `np.argmax()` 和 `np.argmin()` 找极值
  2. 定义阈值：如 NDVI > 0.3 为生长季
  3. 在平滑曲线上标出这些物候点
  4. 保存标注后的图 `outputs/ndvi_phenology.png`
  5. 将物候指标保存为 JSON `data/processed/phenology.json`
- **完成标志**：
  - 图中标注了 NDVI 峰值日期和生长季起止日期
  - 物候指标数值合理
- **常见坑**：阈值选择依赖于研究区的植被类型。农田区（作物）和林地区的阈值不同。

---

### Task 20：对比分析 — 不同植被类型的 NDVI 时序（可选，进阶）

- **Phase**：Phase 3
- **预计耗时**：3 小时
- **依赖任务**：Task 19
- **任务描述**：
  在研究区内选择 2~3 个不同土地利用类型的小区域（如农田、林地、水体），分别提取各自的 NDVI 时间序列，在同一张图中绘制对比折线图。分析不同植被类型的物候差异。
- **具体动作**：
  1. 在 GEE 中为不同区域创建不同的 Geometry
  2. 分别提取各区域的 NDVI 时间序列
  3. 在同一张图中用不同颜色绘制
  4. 添加图例
  5. 保存 `outputs/ndvi_comparison.png`
- **完成标志**：
  - 对比图显示农田、林地、水体的 NDVI 时序明显不同
  - 能解释为什么不同（如农田有收割期，林地 NDVI 更稳定）
- **常见坑**：区域太小 → NDVI 统计不稳定。每个区域至少包含 100 个像素。

---

### ✅ Phase 3 检查点

- [ ] Task 15 ~ 20 全部完成
- [ ] 能解释 NDVI 时间序列中的季节性模式
- [ ] 插值后的均匀序列可用于 FFT

---

## Phase 4：傅里叶频谱分析（Task 21 ~ 26）

---

### Task 21：复习 FFT 基础 — 用简单信号验证 scipy.fft

- **Phase**：Phase 4
- **预计耗时**：3 小时
- **依赖任务**：无（可与 Phase 3 并行）
- **任务描述**：
  不直接对 NDVI 做 FFT。先用人工构造的简单信号（如 sin(2π×0.1×t) + 0.5×sin(2π×0.3×t)）测试 `scipy.fft.fft()`。验证你能从频谱中正确恢复原始信号的频率成分。这是理解 FFT 的关键步骤。
- **具体动作**：
  1. 构造包含两个频率成分的信号：f1=0.1（周期10天），f2=0.3（周期约3.3天）
  2. 使用 `scipy.fft.fft()` 计算频谱
  3. 使用 `scipy.fft.fftfreq()` 计算频率轴
  4. 绘制幅度谱，验证峰值出现在 f1 和 f2 处
  5. 理解频率分辨率 = 1/(N×Δt)
- **完成标志**：
  - 能从幅度谱中准确识别 f1=0.1 和 f2=0.3
  - 能解释：频率轴上的每个点代表什么
  - 笔记写入 NOTES.md
- **常见坑**：fftfreq 和 rfft 的频率轴不同。实数信号用 rfft 更高效。混淆频率单位（Hz vs 周期/天）。

---

### Task 22：对 NDVI 序列执行 FFT 并绘制频谱图

- **Phase**：Phase 4
- **预计耗时**：3 小时
- **依赖任务**：Task 17（插值序列）, Task 21（FFT 基础）
- **任务描述**：
  编写 `src/fft_analyzer.py`。将 Task 17 插值后的 NDVI 序列视为离散信号，执行 `scipy.fft.rfft()` 并绘制幅度谱和功率谱。横轴为频率（1/天）或周期（天），纵轴为幅度/功率。
- **具体动作**：
  1. 读取插值后的 NDVI 序列
  2. 去均值（减去 NDVI 均值），去除直流分量
  3. 执行 `rfft()`
  4. 计算频率轴和周期轴
  5. 绘制两个子图：(a) 幅度谱 vs 周期，(b) 功率谱 vs 周期
  6. 保存 `outputs/ndvi_spectrum.png`
- **完成标志**：
  - 频谱图中能看到明显的峰值
  - 能大致说出最大峰值对应的周期（如 ~365 天）
- **常见坑**：去均值很重要，否则 0 频率（直流分量）会淹没其他成分。周期轴 = 1/频率，注意单位换算。

---

### Task 23：从频谱中提取 Top 3 主周期

- **Phase**：Phase 4
- **预计耗时**：2 小时
- **依赖任务**：Task 22
- **任务描述**：
  扩展 `src/fft_analyzer.py`，从频谱中自动提取振幅最大的 3 个频率分量，换算为周期（天数），并按振幅降序输出。在频谱图上标注这 3 个主周期的位置。
- **具体动作**：
  1. 取幅度谱中最大的 3 个峰值（排除 0 频率）
  2. 对应的频率 → 周期（天数）= 1/频率
  3. 打印 Top 3：周期1=365天（年周期）、周期2=182天（半年周期）、周期3=?
  4. 在频谱图上用红色竖线标注
  5. 保存标注后的图
- **完成标志**：
  - 终端输出 Top 3 主周期
  - 图中标注了 3 个峰值位置
- **常见坑**：峰值检测容易选到旁瓣。需要设置最小峰值距离参数 `scipy.signal.find_peaks()`。

---

### Task 24：解释频谱的物理含义 — 写分析笔记

- **Phase**：Phase 4
- **预计耗时**：2 小时
- **依赖任务**：Task 23
- **任务描述**：
  这是整个项目中最重要的"学习型"Task。不是写代码，而是用人话解释 Task 23 提取的主周期分别代表什么。例如：年周期（365天）= 一年四季的植被变化；半年周期（182天）= 双季作物或年内的二次波动。将分析写入 NOTES.md 和 DECISIONS.md。
- **具体动作**：
  1. 分析每个主周期可能的物理含义
  2. 结合研究区的实际植被类型（郓城县主要是冬小麦-夏玉米轮作）
  3. 写至少 500 字的分析笔记
  4. 将傅里叶分析结论写入 DECISIONS.md
- **完成标志**：
  - NOTES.md 新增傅里叶分析笔记
  - 能口头向非遥感专业的人解释频谱图
- **常见坑**：不要把"周期=365天"当作发现 — 这是一年四季的必然结果。关注的是非 365 天的周期。

---

### Task 25：对比不同年份的 NDVI 频谱（可选，进阶）

- **Phase**：Phase 4
- **预计耗时**：3 小时
- **依赖任务**：Task 24
- **任务描述**：
  如果有 2024 年或更早的数据，重复 Task 22~23，对比两个年份的 NDVI 频谱差异。分析年际变化是否显著。
- **具体动作**：
  1. 在 GEE 中获取 2024 年同区域的影像
  2. 重复 NDVI → 时序 → FFT 流程
  3. 将两年频谱并排绘制
  4. 分析差异
- **完成标志**：
  - 两年频谱对比图
  - 分析笔记
- **常见坑**：如果 2024 年数据不足（云量多），先跳过此 Task。

---

### Task 26：编写 FFT 分析模块的完整 docstring 和注释

- **Phase**：Phase 4
- **预计耗时**：1.5 小时
- **依赖任务**：Task 24
- **任务描述**：
  回顾 `src/fft_analyzer.py`，为每个函数编写完整的 docstring。确保代码清晰、有注释、三个月后能看懂。这有助于复试时展示代码质量。
- **具体动作**：
  1. 为每个函数写 docstring（参数、返回值、功能描述）
  2. 关键行添加注释（解释为什么这样做）
  3. 在文件开头写模块说明
- **完成标志**：
  - `src/fft_analyzer.py` 每个函数都有 docstring
  - 代码可读性良好
- **常见坑**：不要过度注释显而易见的内容。注释应解释"为什么"，而不是"什么"。

---

### ✅ Phase 4 检查点

- [ ] Task 21 ~ 26 全部完成
- [ ] `outputs/ndvi_spectrum.png` 存在且标注了主周期
- [ ] 能用人话解释频谱图的含义
- [ ] FFT 分析结果能在复试中讲 5 分钟

---

## Phase 5：可视化与 PDF 报告（Task 27 ~ 33）

---

### Task 27：设计 PDF 报告的章节结构

- **Phase**：Phase 5
- **预计耗时**：2 小时
- **依赖任务**：无（纯设计 Task）
- **任务描述**：
  不写代码。在白纸/Notion/VS Code 中设计 PDF 报告的章节结构。确定：封面信息、每章标题、每章包含的图表类型、页码、报告总体页数（建议 8~12 页）。
- **具体动作**：
  1. 列出报告结构（大纲）
  2. 确定每章需要的图表
  3. 画出每页的布局草图
  4. 写入 `docs/report_design.md`
- **完成标志**：
  - `docs/report_design.md` 包含完整的报告结构
  - 至少 6 个章节
- **常见坑**：不要追求花哨的设计。学术报告的核心是清晰、专业、可复现。

---

### Task 28：安装 fpdf2 并生成第一页 PDF（封面）

- **Phase**：Phase 5
- **预计耗时**：2.5 小时
- **依赖任务**：Task 27
- **任务描述**：
  安装 `fpdf2` 库，编写 `src/report_gen.py`，生成只有封面的 PDF。封面包含：报告标题、研究区域名称、分析时间范围、生成日期、作者信息。解决中文字体问题。
- **具体动作**：
  1. `pip install fpdf2`
  2. 下载一个免费中文字体（如思源黑体）放到 `data/fonts/`
  3. 使用 fpdf2 的 `add_font()` 注册中文字体
  4. 创建封面页：标题居中、信息列表
  5. 输出 `outputs/report_test.pdf`
- **完成标志**：
  - `outputs/report_test.pdf` 存在
  - 封面中文正常显示，不乱码
- **常见坑**：**中文字体是最大坑**。大多数 PDF 库默认不支持中文。必须手动注册 .ttf 字体。参考 RISK.md。

---

### Task 29：在地图中叠加研究区边界和 NDVI

- **Phase**：Phase 5
- **预计耗时**：3 小时
- **依赖任务**：Task 10
- **任务描述**：
  编写 `src/visualizer.py`，使用 matplotlib（+ cartopy 可选）生成一张高质量的研究区地图。叠加 Sentinel-2 真彩色底图和研究区边界。标注经纬度网格、指北针、比例尺。
- **具体动作**：
  1. 使用 rasterio 读取影像的地理范围
  2. 使用 `ax.imshow()` 显示真彩色影像，设置正确的 extent
  3. 如果不用 cartopy，手动设置坐标轴标签为经纬度
  4. 添加网格线
  5. 保存 `outputs/study_area_map.png`（300 dpi）
- **完成标志**：
  - 地图清晰显示研究区位置和范围
  - 分辨率 300 dpi，适合嵌入 PDF
- **常见坑**：extent 参数顺序是 (left, right, bottom, top)，注意不要写成 (left, right, top, bottom)。

---

### Task 30：美化 NDVI 时序图（出版物级别）

- **Phase**：Phase 5
- **预计耗时**：3 小时
- **依赖任务**：Task 15, Task 18, Task 19
- **任务描述**：
  将 Task 15~19 中粗糙的折线图升级为"可以放进 PDF 报告"的级别。要求：合适的字体大小、清晰的图例、标注物候期、专业配色。使用 matplotlib 的 rcParams 全局设置。
- **具体动作**：
  1. 设置 matplotlib 全局样式（字体、字号、线宽）
  2. 绘制 NDVI 时序图：平滑线 + 原始散点 + 异常标记 + 物候标注
  3. 添加中文标题和轴标签
  4. 保存 `outputs/ndvi_timeseries_final.png`（300 dpi）
- **完成标志**：
  - 时序图能直接放入 PDF 报告
  - 配色专业、标注清晰
- **常见坑**：matplotlib 中文显示。需要设置 `plt.rcParams['font.sans-serif']`。

---

### Task 31：美化 FFT 频谱图（出版物级别）

- **Phase**：Phase 5
- **预计耗时**：2 小时
- **依赖任务**：Task 23
- **任务描述**：
  将 Task 22~23 的频谱图升级为出版物级别。标注主周期、添加中英文混合标题、使用专业配色。
- **具体动作**：
  1. 美化幅度谱图
  2. 在主周期峰值添加文字标注（如 "365天"）
  3. 使用 log 尺度显示纵轴（可选）
  4. 保存 `outputs/ndvi_spectrum_final.png`（300 dpi）
- **完成标志**：
  - 频谱图可直接放入 PDF 报告
- **常见坑**：频谱图的横轴标注。建议同时显示频率（1/天）和周期（天）两种刻度。

---

### Task 32：生成完整的第一版 PDF 报告

- **Phase**：Phase 5
- **预计耗时**：3 小时
- **依赖任务**：Task 28, Task 29, Task 30, Task 31
- **任务描述**：
  编写完整的 PDF 生成脚本。将 Task 28~31 生成的所有图表嵌入 PDF，按 Task 27 设计的章节结构排列。添加页码、页眉、目录。这是第一个"可以拿出去给人看"的版本。
- **具体动作**：
  1. 按章节顺序添加页面
  2. 每章：标题 → 描述文字 → 图表
  3. 添加页码（footer）
  4. 添加封面和目录页
  5. 输出 `outputs/report_v1.pdf`
- **完成标志**：
  - 一份 8~12 页的 PDF 报告
  - 包含封面、目录、研究区地图、NDVI 图、时序图、频谱图、统计表、结论
- **常见坑**：图片尺寸和 PDF 页面尺寸的匹配。插入图片前需要调整图片 DPI。

---

### Task 33：PDF 报告内容审查与修改

- **Phase**：Phase 5
- **预计耗时**：2 小时
- **依赖任务**：Task 32
- **任务描述**：
  仔细审查第一版 PDF 报告：检查文字描述是否准确、图表是否清晰、逻辑是否通顺。假想自己是复试导师，读这份报告会有什么问题。修改至少 3 处内容问题。
- **具体动作**：
  1. 打印 PDF（或屏幕阅读），逐页审查
  2. 标记所有问题（文字、图表、格式）
  3. 修改并重新生成
  4. 输出 `outputs/report_v2.pdf`
- **完成标志**：
  - 自己读一遍不觉得尴尬
  - 每个图都有对应的文字解读
- **常见坑**：学生容易只放图不解释。复试导师想看的是"你能从图中读出什么"，而不是"你会画图"。

---

### ✅ Phase 5 检查点

- [ ] Task 27 ~ 33 全部完成
- [ ] `outputs/report_v2.pdf` 可直接用于复试展示
- [ ] 所有图表 300 dpi
- [ ] 中文显示正常

---

## Phase 6：系统集成与打磨（Task 34 ~ 40）

---

### Task 34：实现地名→坐标转换

- **Phase**：Phase 6
- **预计耗时**：2.5 小时
- **依赖任务**：无
- **任务描述**：
  编写 `src/geocode.py`，将用户输入的地名（如"山东省菏泽市郓城县"）转换为经纬度坐标。可以使用简单方案（预定义字典），也可以使用 geopy 库调用 Nominatim 服务。目标是让用户不需要手动输入坐标。
- **具体动作**：
  1. 方案A：预定义字典 `{"郓城县": (115.9, 35.6)}` — 简单但有限
  2. 方案B：`geopy.geocoders.Nominatim` — 需要网络
  3. 选择方案并实现
  4. 测试：输入"郓城县"，输出 (115.94, 35.60)
  5. 返回的坐标用于在 GEE 中创建 Geometry（如 0.1° buffer 的矩形）
- **完成标志**：
  - `geocode("郓城县")` 返回合理的经纬度
  - 能处理中文地名
- **常见坑**：Nominatim 对中文地名支持一般。建议先用预定义字典 + 少量地名，后续再扩展。

---

### Task 35：创建 config.yaml 配置系统

- **Phase**：Phase 6
- **预计耗时**：2 小时
- **依赖任务**：所有功能模块
- **任务描述**：
  创建 `config.yaml`，将所有硬编码的参数集中管理。包括：研究区域名称/坐标、年份、云量阈值、输出路径、NDVI 计算参数、FFT 参数、PDF 设置等。使用 PyYAML 读取配置。
- **具体动作**：
  1. `pip install pyyaml`
  2. 设计 config.yaml 结构
  3. 编写 `src/config.py` 加载配置
  4. 修改各模块使用配置而非硬编码
- **完成标志**：
  - 修改年份/区域只需改 config.yaml，不需要改代码
  - `python main.py --config config.yaml` 能运行
- **常见坑**：路径在 Windows 和 Linux 上的分隔符不同。统一使用 `/` 或 `os.path.join()`。

---

### Task 36：编写 pipeline.py — 一键运行主流程

- **Phase**：Phase 6
- **预计耗时**：3 小时
- **依赖任务**：Task 34, Task 35
- **任务描述**：
  编写 `src/pipeline.py`（或 `main.py`），将全部流程串联为一条命令：`python main.py --region 郓城县`。流程步骤：地名解析 → GEE 数据获取 → NDVI 计算 → 时间序列 → FFT → 可视化 → PDF 生成。每步完成后打印进度信息。
- **具体动作**：
  1. 导入所有模块
  2. 编写 `run_pipeline(region_name)` 函数
  3. 使用 argparse 解析命令行参数
  4. 每步 try/except，失败时打印友好错误信息
  5. 运行时打印进度：[1/7] 获取影像... [2/7] 计算 NDVI...
- **完成标志**：
  - `python main.py --region 郓城县` 一键生成完整 PDF
  - 中间文件正确保存到 data/processed/ 和 outputs/
- **常见坑**：GEE 认证过期。首次运行需要 `ee.Authenticate()` 和 `ee.Initialize()`。

---

### Task 37：增加日志系统

- **Phase**：Phase 6
- **预计耗时**：2 小时
- **依赖任务**：Task 36
- **任务描述**：
  使用 Python logging 模块替换所有 `print()`。日志同时输出到终端和文件 `logs/pipeline.log`。记录：时间戳、步骤名称、成功/失败状态、参数信息。
- **具体动作**：
  1. 配置 logging：格式 = `[时间] [级别] 消息`
  2. 设置两个 handler：StreamHandler（终端）+ FileHandler（文件）
  3. 在 pipeline.py 和各模块中使用 `logging.info()` 替代 `print()`
  4. 关键步骤使用 `logging.warning()` 和 `logging.error()`
- **完成标志**：
  - 终端有进度输出
  - `logs/pipeline.log` 记录完整的运行历史
- **常见坑**：logging 多次配置导致重复输出。在 `main.py` 中统一配置一次。

---

### Task 38：编写测试脚本

- **Phase**：Phase 6
- **预计耗时**：3 小时
- **依赖任务**：Task 36
- **任务描述**：
  编写 `tests/test_modules.py`，对核心函数进行基本的功能测试。不追求覆盖率，只验证核心逻辑正确。例如：`test_ndvi_calculation()` 验证 NDVI 公式正确性（已知输入 → 已知输出）。
- **具体动作**：
  1. 创建 `tests/` 目录
  2. 编写测试用例：
     - `test_ndvi()`：输入 (red=0.1, nir=0.5) → 期望输出 (0.5-0.1)/(0.5+0.1)=0.667
     - `test_fft()`：输入 sin 信号 → 验证频谱峰值频率
     - `test_geocode()`：输入"郓城县" → 期望返回合理经纬度
  3. 使用 pytest 运行
- **完成标志**：
  - `pytest` 全部通过
  - 至少 5 个测试用例
- **常见坑**：测试数据路径问题。使用相对路径时注意当前工作目录。

---

### Task 39：在 README.md 中补充完整使用说明

- **Phase**：Phase 6
- **预计耗时**：2 小时
- **依赖任务**：Task 36
- **任务描述**：
  完善 `README.md`，使其达到开源项目标准。包含：项目简介、效果截图、安装步骤、使用示例、项目结构说明、常见问题。目标是：任何人（包括复试导师）都能根据 README 了解这个项目。
- **具体动作**：
  1. 添加项目徽章（Python 版本、License）
  2. 添加效果截图（PNG 预览）
  3. 写安装步骤（clone → pip install → GEE 认证）
  4. 写使用示例（3 种场景）
  5. 写项目结构说明
  6. 写 FAQ
- **完成标志**：
  - README.md 内容完整
  - GitHub 页面看起来专业
- **常见坑**：截屏文件太大，需要压缩后再放入 README。

---

### Task 40：为 3 个不同类型的区域生成示例报告

- **Phase**：Phase 6
- **预计耗时**：3 小时
- **依赖任务**：Task 36, Task 32
- **任务描述**：
  选择 3 个不同类型的区域（如：郓城县=农田为主、某城市区域=建筑为主、某林区=森林为主），分别运行完整流程，生成 3 份 PDF 报告。这些是最终的作品集展示物。
- **具体动作**：
  1. 确定 3 个示例区域
  2. 分别运行 `python main.py --region X`
  3. 检查每份报告的完整性和正确性
  4. 将 3 份 PDF 放到 `outputs/examples/`
- **完成标志**：
  - `outputs/examples/` 中有 3 份 PDF
  - 每份报告根据区域特征有不同的分析结论
- **常见坑**：城市区域 NDVI 低，FFT 可能没有明显的周期。这是正常的，在报告中解释即可。

---

### ✅ Phase 6 检查点（= 项目完成）

- [ ] Task 34 ~ 40 全部完成
- [ ] `python main.py --region 郓城县` 一键生成完整 PDF
- [ ] 3 份示例报告
- [ ] README 完善
- [ ] 测试通过

---

## 附录：Task 总览表

| Task | Phase | 名称 | 预计耗时 | 核心技能 |
|------|-------|------|----------|----------|
| 01 | 1 | ✅ GEE 导出第一张 GeoTIFF | 2h | GEE Export |
| 02 | 1 | ✅ 下载到本地 data/raw/ | 1h | 文件管理 |
| 03 | 1 | rasterio 读取元数据 | 2h | rasterio |
| 04 | 1 | 提取 B4/B8 为 numpy 数组 | 2h | numpy |
| 05 | 1 | matplotlib 显示真彩色 | 3h | matplotlib |
| 06 | 1 | 批量导出 28 景影像 | 3h | GEE batch |
| 07 | 1 | 批量读取元数据汇总 | 2h | glob+rasterio |
| 08 | 2 | 手动计算一个像素的 NDVI | 1.5h | NDVI 原理 |
| 09 | 2 | 编写 NDVI 计算函数 | 2h | numpy, rasterio 写入 |
| 10 | 2 | 生成 NDVI 伪彩色图 | 2h | matplotlib colormap |
| 11 | 2 | GEE 云端计算 NDVI | 3h | GEE .map() |
| 12 | 2 | 批量 NDVI 均值 → CSV | 3h | 批量处理, csv |
| 13 | 2 | GEE 时序图 | 2h | GEE Chart |
| 14 | 2 | 确定技术方案 | 1h | 决策记录 |
| 15 | 3 | 绘制原始 NDVI 折线图 | 2h | matplotlib 时序 |
| 16 | 3 | 异常值检测 | 2.5h | 统计方法 |
| 17 | 3 | 线性插值均匀采样 | 2.5h | numpy.interp |
| 18 | 3 | 滑动平均平滑 | 2h | 信号处理 |
| 19 | 3 | 提取物候指标 | 3h | 物候学 |
| 20 | 3 | 多类型对比（可选） | 3h | 对比分析 |
| 21 | 4 | FFT 基础验证 | 3h | scipy.fft |
| 22 | 4 | NDVI FFT → 频谱图 | 3h | rfft, 频谱 |
| 23 | 4 | 提取 Top 3 主周期 | 2h | 峰值检测 |
| 24 | 4 | 频谱含义分析笔记 | 2h | 领域知识 |
| 25 | 4 | 多年对比（可选） | 3h | 年际分析 |
| 26 | 4 | 代码 docstring | 1.5h | 代码规范 |
| 27 | 5 | PDF 报告结构设计 | 2h | 报告设计 |
| 28 | 5 | fpdf2 封面页 | 2.5h | fpdf2, 中文字体 |
| 29 | 5 | 研究区地图 | 3h | 地图可视化 |
| 30 | 5 | 美化 NDVI 时序图 | 3h | matplotlib 美化 |
| 31 | 5 | 美化 FFT 频谱图 | 2h | matplotlib 美化 |
| 32 | 5 | 生成第一版 PDF | 3h | fpdf2 整合 |
| 33 | 5 | 报告内容审查 | 2h | 内容审查 |
| 34 | 6 | 地名→坐标 | 2.5h | geopy/geocoding |
| 35 | 6 | config.yaml | 2h | PyYAML |
| 36 | 6 | pipeline.py 一键运行 | 3h | 流程编排 |
| 37 | 6 | logging 日志系统 | 2h | logging |
| 38 | 6 | 测试脚本 | 3h | pytest |
| 39 | 6 | README 完善 | 2h | 文档 |
| 40 | 6 | 3 份示例报告 | 3h | 完整流程 |

**总计：40 个 Task，约 96 小时**

> 注意：96 小时是紧凑估算。实际可能有卡点、返工、深入学习。按每天 3 小时算，约 32 天完成任务核心部分。但 Phase 之间的学习、消化、写笔记、试错需要额外时间。这也是为什么总时间线拉长到 6 个月（约 180 天 × 3h = 540h）—— 留足缓冲。
