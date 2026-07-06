# 今日任务

## 当前阶段26年7月1日
一战：GeoTIFF 驯服战

## 今天完成
- [√] 创建项目目录
- [√] 创建文档体系（README、PROJECT、TODAY、DECISIONS、CHANGELOG）
- [√] 创建 Python 虚拟环境
- [√] 安装 numpy、matplotlib、rasterio
- [√ 验证 Python 开发环境（check_env.py）
- [√] 创建 data/raw、data/processed、outputs、scripts 目录
- [√] 注册 Google Earth Engine（非商业项目）

## 当前卡点
- 暂无

## 明天计划
- [√] 学习 GeoTIFF 基础概念
- [√] 获取第一张 Sentinel-2 GeoTIFF
- [√] 使用 rasterio 读取 GeoTIFF 元数据



# TODAY

## 日期

2026-07-02

---

## 今天完成了什么？

完成了 Google Earth Engine 第一战的重要阶段：

- 学会使用 Geometry 作为研究区域
- 理解了 Geometry 与行政区名称的区别
- 使用 filterBounds() 进行空间筛选
- 使用 filterDate() 进行时间筛选
- 使用 filter() + CLOUDY_PIXEL_PERCENTAGE 进行云量过滤
- 成功筛选出符合条件的 Sentinel-2 数据

最终筛选结果：

Global Sentinel-2
↓

研究区

↓

2025 年

↓

云量 <10%

↓

28 张 Sentinel-2 影像

---

## 今天学会的新知识

理解了：

ImageCollection 并不是一张影像。

经过 filterBounds()、filterDate() 后，
得到的仍然是 ImageCollection。

filter() 可以根据影像属性继续筛选。

Sentinel-2 数据集自带云量属性：

CLOUDY_PIXEL_PERCENTAGE

可以用于自动筛选高质量影像。

---

## 今天踩过的坑

- ImageCollection 拼写错误
- geometry 重复定义
- JavaScript 分号导致链式调用中断
- lt 写成 1t（数字1）

开始理解如何阅读报错信息，
而不是只看代码变红。

---

## 下一步

学习：

dataset.first()

理解：

ImageCollection

↓

Image

然后显示第一张真正可分析的 Sentinel-2 影像。


## 2026-07-03

### 今天完成

- [√] 学习 dataset.first()：ImageCollection → Image
- [√] 第一次显示真正的 Sentinel-2 真彩色影像（B4/B3/B2）
- [√] 理解 B2/B3/B4/B8 每个波段含义
- [√] 学习 Export.image.toDrive() 全部参数
- [√] 解决导出 Bug：UInt16 与 Byte 数据类型不兼容 → select() 只导出需要的波段
- [√] 成功导出 sentinel2_sample.tif 到 Google Drive
- [√] 下载 GeoTIFF 到 data/raw/sentinel2_sample.tif

### 今天踩坑

1. 忘记 Ctrl+S 保存 GEE 代码 → 刷新后代码丢失 → 以后先保存再 Run
2. 导出全部波段报错：UInt16 与 Byte 不一致 → 用 select(['B2','B3','B4','B8']) 解决
3. JavaScript 对象漏写逗号 → 养成检查语法的习惯

### 当前卡点

- 暂无

### 明天计划

- [√] 使用 rasterio 读取 sentinel2_sample.tif 并打印元数据
- [√] 提取 B4 和 B8 波段为 numpy 数组
- [ ] 使用 matplotlib 显示真彩色影像


## 2026-07-04

### ✅ Task 03 完成：rasterio 读取 GeoTIFF 元数据

编写 `src/read_geotiff.py`，使用 rasterio 打开 `data/raw/sentinel2_sample.tif`，成功打印全部元数据：

- CRS（坐标参考系）、Bounds（地理范围）、Transform（仿射变换）
- Width（216 像素）、Height（174 像素）、Band Count（4 个波段）
- Dtypes（uint16）、Band Descriptions

### ✅ Task 04 完成：提取 B4/B8 为 numpy 数组并打印统计信息

从 GeoTIFF 中读取 Red（导出的 Band 3 = S2 B4）和 NIR（导出的 Band 4 = S2 B8），转为 `float32` 并统计 min / max / mean / std / shape / dtype。

### ✅ 新增：NDVI 首次计算

使用 NumPy Element-wise Operation 批量计算整景 NDVI：
```python
ndvi = (b8 - b4) / (b8 + b4)
```
得到 216×174 的 NDVI 数组（float32），打印 min / max / mean / std。

---

### 今天学到的新概念（重点）

| 概念 | 结合项目的理解 |
|------|---------------|
| **DatasetReader** | `rasterio.open()` 返回读取器，不是数据本身。Lazy Reading：需要哪个波段才读哪个 |
| **ndarray** | `dataset.read(3)` 返回的是 `numpy.ndarray`，不是 Python list，是一个二维矩阵 |
| **shape** | `b4.shape` → `(174, 216)`，174 行（高度）× 216 列（宽度） |
| **dtype** | 数据类型。原始 GeoTIFF 是 `uint16`（0~65535 的整数），转 `float32` 后才能做除法 |
| **uint16** | Sentinel-2 L2A 将地表反射率 × 10000 存储为整数，0~10000 范围 |
| **float32** | 转为 32 位浮点数，NDVI 值是小数（-1~1），必须用浮点类型 |
| **Element-wise Op** | `(b8 - b4) / (b8 + b4)` 一次性对 216×174 个像素同时运算，无需 for 循环 |
| **NDVI** | 归一化植被指数 = (NIR - Red) / (NIR + Red)，值域 -1~1，>0.3 通常表示植被 |
| **NIR** | 近红外（B8），植被在近红外波段强反射，是 NDVI 的核心 |
| **Reflectance** | 地表反射率，Sentinel-2 L2A 数据已做大气校正，DN/10000 = 真实反射率 |

### 今天踩坑

1. pip install pyyaml vs import yaml：安装名和导入名不同
2. 误以为 width 是米的宽度，实际是像素数量
3. 误以为 dataset.read(1) 读的是 Sentinel-2 Band 1，实际是导出文件第 1 个波段
4. 原始 uint16 直接做除法 → 结果也是整数 → 必须先 `.astype('float32')`

### 当前卡点

- 暂无

### 明天计划（Task 05）

- [√] 使用 matplotlib 显示 Sentinel-2 真彩色影像（B4-B3-B2）
- [√] 对数据进行 2%~98% 拉伸（clip），增强对比度
- [√] 使用 extent 设置真实地理坐标轴

---

### 今日遇到的问题（8 个）

#### 1. PyYAML 未安装

**现象**：VS Code 中 `import yaml` 出现黄色波浪线。

**第一反应（错误思路）**：以为 config.py 写错了 / VS Code 出 Bug 了 / 代码有语法错误。

**实际原因**：Python 环境没有安装 PyYAML，VS Code 的 Pylance 无法解析 `import yaml`。

**排查过程**：
1. 运行 `pip show pyyaml` → `Package(s) not found`，确认未安装
2. 运行 `pip install pyyaml` → 问题解决

**学到的知识**：很多 Python 库 **安装名称 ≠ 导入名称**：

| 安装名 | 导入名 |
|--------|--------|
| pyyaml | yaml |
| opencv-python | cv2 |
| pillow | PIL |
| scikit-learn | sklearn |

---

#### 2. VS Code 的黄色数字不是报错

**现象**：文件 tab 上显示黄色数字 `1`，以为程序报错。

**实际情况**：`Problems = 1`，表示当前文件存在一个 Warning / Problem，不是程序运行失败。

**学到的知识**：VS Code 黄色数字 = Problems 面板提示。程序是否运行成功应该看 **Terminal**，不是看编辑器标签页。

---

#### 3. 不知道如何运行 Python

**现象**：第一次不知道 `python src/read_geotiff.py` 应该在哪里执行。

**解决**：学习使用 VS Code Terminal，在终端中运行 Python 脚本。

**学到的知识**：以后所有 Python 程序都通过 Terminal 运行，不要只看编辑器。

---

#### 4. 误以为程序没有输出就是失败

**现象**：运行 `dataset = rasterio.open(...)` 后终端没有任何输出，以为程序没运行。

**实际情况**：程序已成功执行，只是代码里没有 `print()`，所以终端不显示任何内容。

**学到的知识**：Python 没有 `print()` 就不会输出，这不是 Bug。

---

#### 5. 混淆了 Pixel 和真实距离

**现象**：看到 `dataset.width = 216`，第一反应是"宽度 216 米？"

**纠正**：216 表示 216 个 Pixel。真正宽度 = 216 × Resolution（10m）= 2160m。

**学到的知识**：`width` / `height` 的单位是**像素数量**，不是米。

---

#### 6. 混淆了 GeoTIFF 波段编号和 Sentinel 波段编号

**现象**：看到 `dataset.read(1)`，容易想成"读取 Sentinel-2 的 B1"。

**纠正**：GeoTIFF 中 Band1 = 导出的第一个波段 = Sentinel-2 B2（按 select(['B2','B3','B4','B8']) 顺序）。

**学到的知识**：`dataset.read(1)` 读取的是**导出文件中第 1 个波段**，不是 Sentinel-2 原始 Band 编号。

---

#### 7. 误以为 dataset.read() 返回一个数字

**现象**：觉得 `dataset.read(1)` 应该返回一个数值。

**纠正**：实际上返回的是整个波段的数据——一个 216×174 的二维矩阵，不是单个像素值。

**学到的知识**：`dataset.read()` 返回 numpy 二维数组，包含该波段的全部像素。

---

#### 8. 今天真正建立的认知（最大收获）

今天最大的收获不是学会了几个 API，而是建立了完整的数据流理解：

```
GeoTIFF 文件
        │
        ▼
DatasetReader（读取器，不是数据本身）
        │
        ├── width / height（像素数量）
        ├── count（波段数量）
        ├── crs / transform（地理信息）
        └── read(band_index)
                │
                ▼
        一个波段的二维矩阵（numpy array）
                │
                ▼
        每个像素对应地球上的同一个位置
                │
                ▼
        不同波段逐像素一一对应 → 计算 NDVI
```

---

---

## 2026-07-05

### ✅ Task 05 完成：Matplotlib 显示 Sentinel-2 真彩色影像

编写 `src/show_rgb.py`，使用 matplotlib 成功显示研究区 Sentinel-2 真彩色影像。

**完成内容**：
- [√] 使用 `np.stack([b4, b3, b2], axis=-1)` 合成 (H, W, 3) RGB 数组
- [√] 对数据进行 2%~98% Clip + Normalize，解决原始数据显示全白问题
- [√] 使用 `extent` 参数设置真实地理坐标轴
- [√] 建立了遥感影像显示的标准流程

**标准显示流程**：
```
GeoTIFF → 读取 B2/B3/B4 → Stack RGB → Clip(2%, 98%) → Normalize(0,1) → imshow + extent → 真实地理坐标
```

### 今天学到的核心概念（15 项）

| # | 概念 | 一句话理解 |
|---|------|-----------|
| 1 | 真彩色合成 | B4→R, B3→G, B2→B，不是随机组合 |
| 2 | RGB 图像本质 | (H, W, 3) 三维数组，最后一个维度是颜色通道 |
| 3 | np.stack(axis=-1) | 沿最后一个轴堆叠，得到 (H,W,3) 而非 (3,H,W) |
| 4 | plt.imshow() | Matplotlib 可直接显示 (H,W,3) 的 RGB ndarray |
| 5 | 影像发白原因 | 遥感 DN 值 87~3580，imshow 对 float 要求 0~1，>1 被裁为 1 |
| 6 | Clip | `np.clip(rgb, low, high)` — 去除异常值，不是修改真实数据 |
| 7 | Normalize | `(rgb - low) / (high - low)` — 映射到 0~1 |
| 8 | 先 Clip 再 Normalize | 直接 Normalize → 极端值占据动态范围 → 对比度低 |
| 9 | np.percentile() | 无 axis 参数时对整个 ndarray 所有元素统一计算 |
| 10 | extent | `[left, right, bottom, top]` 让 imshow 显示真实坐标 |
| 11 | 像素坐标 vs 地理坐标 | imshow 默认不知道 GeoTIFF 空间位置，需 extent 告知 |
| 12 | 2%~98% 拉伸 | 教材里的"2%~98% 拉伸"就是今天做的 Clip + Normalize |
| 13 | 遥感算法本质 | 绝大多数遥感算法 = NumPy 数组上的数学运算 |
| 14 | NDVI 与 RGB 合成的共性 | 都是逐像素数组运算：NDVI 是逐元素四则运算，RGB 是数组堆叠 |
| 15 | 显示失败排查链 | 显示发白 → 检查 dtype → 检查范围 → Clip → Normalize → 成功 |

### 今天踩过的坑

1. **第一次 `plt.imshow(rgb)` 图像一片白**
   - 原因：未做 Clip 和 Normalize，DN 值 87~3580 远超 0~1
   - 解决：先 Clip(2%, 98%) → Normalize(0, 1) → 正常显示

2. **第一次显示坐标是 0~220（像素坐标）**
   - 原因：imshow 默认使用像素坐标
   - 解决：设置 `extent=[bounds.left, bounds.right, bounds.bottom, bounds.top]`

### 今天最大的收获

把期末考试中的"2%~98% 拉伸"和真实工程中的遥感影像显示联系了起来。以前知道要做 2%~98% 拉伸，但不知道为什么。今天通过 Matplotlib 的警告信息，真正理解了为什么需要 Clip、为什么需要 Normalize、为什么不能直接显示原始遥感数据。

**核心理念**：教材、考试和工程实践，其实是在解决同一个问题。

### 当前卡点

- 暂无

### 明天计划（Task 06）

- [√] 理解 ImageCollection 不能直接 Export（需要逐张拆开）
- [√] 理解 GEE Server-side vs Client-side 运行机制
- [√] 理解 evaluate() / getInfo() / toList() / get() / ee.Image() 类型转换
- [√] 理解工程化文件命名（S2_yyyyMMdd）

### Tech Lead 评价

今天遇到的问题几乎都不是代码错误，而是**概念上的误区**：

1. Python 包安装与导入名称的区别
2. VS Code 警告与运行错误的区别
3. Pixel 与真实地面距离的区别
4. GeoTIFF 波段编号与 Sentinel 波段编号的区别
5. 读取器（DatasetReader）与实际数据的区别
6. 程序无输出 vs 程序未运行的区别
7. 单个数值 vs 二维矩阵的区别

这些都是遥感工程初学者最容易混淆的地方。今天把它们逐一澄清，比多写几十行代码更有价值，因为它们会直接影响后续 NDVI、NDWI、EVI、时序分析等所有模块的理解。


## 2026-07-07

### ✅ Task 06（前半）：GEE 批量导出 — Server-side 与 Client-side 机制深入理解

今天没有追求快速写代码，而是重点理解 GEE 的运行机制——这是 Task 06 批量导出的理论基础。

**核心认知突破**：理解了为什么 GEE 不能像普通 Python/JavaScript 那样写 for 循环。

### 今天学到的核心概念（13 项）

| # | 概念 | 一句话理解 |
|---|------|-----------|
| 1 | ImageCollection 不能直接 Export | Export 要求 ee.Image，不是 ee.ImageCollection，必须逐张拆开 |
| 2 | toList(n) | ImageCollection → ee.List，才能按索引访问 |
| 3 | size() | 返回 ee.Number（服务器对象），不是 JavaScript Number |
| 4 | Server-side Object | ee.Image / ee.ImageCollection / ee.Number / ee.List / ee.Date — 存在于 Google 服务器 |
| 5 | Client-side Object | JavaScript Number / String / Array / for 循环 — 存在于浏览器 |
| 6 | evaluate() | ee.Number → JavaScript Number，异步回调方式 |
| 7 | getInfo() | 同步等待服务器返回（工程中少用，优先 evaluate） |
| 8 | ee.List.get(i) | ee.List 不能 `[i]`，必须 `.get(i)` |
| 9 | ee.Image() 类型转换 | get() 返回 Object → ee.Image() 强转后才能调用 select() 等 API |
| 10 | image.date().format() | ee.Date → 格式化字符串，用于工程化文件命名 |
| 11 | 循环边界 i < n | n=28 → i=0..27，不是 0..28 |
| 12 | print() vs evaluate() | print() 只是显示，evaluate() 才是类型转换 |
| 13 | 为什么 dataset.first() 不够 | 时间序列分析需要 28 景全部影像，不是只有一景 |

### 今天学到的核心机制：Server-side vs Client-side

**GEE 不是在你的浏览器里跑代码**。GEE 代码在 Google 服务器上执行，浏览器只是发送指令和接收结果。

```
┌─────────────────────────┐     ┌─────────────────────────┐
│   浏览器（Client-side）    │     │   Google 服务器（Server-side） │
│                         │     │                         │
│  JavaScript Number      │ ◀── │  ee.Number              │
│  String                 │ ◀── │  ee.String              │
│  Array                  │ ◀── │  ee.List                │
│  for 循环               │     │  .map() 批量处理         │
│                         │     │                         │
│  evaluate() ────────────│───▶ │  计算                    │
│  getInfo() ─────────────│───▶ │  计算（同步等待）         │
└─────────────────────────┘     └─────────────────────────┘
```

**关键理解**：
- `count = dataset.size()` → `ee.Number`（还在服务器上）
- `count.evaluate(function(n){...})` → `n = 28`（真正回到浏览器的数字）
- `for(var i=0; i<count; i++)` ❌ — ee.Number 不能用于 for 循环
- `for(var i=0; i<n; i++)` ✅ — JavaScript Number 才能用 for

### 今天建立的完整数据流

```
ImageCollection (28景)
    │
    ▼
.size() → ee.Number(28)
    │
    ▼
.evaluate(function(n){...}) → JavaScript Number(28)
    │
    ▼
.toList(n) → ee.List
    │
    ▼
for(var i=0; i<n; i++)
    │
    ▼
ee.Image(imageList.get(i)) → ee.Image
    │
    ▼
.date().format("yyyyMMdd") → 文件名 "S2_20250315"
    │
    ▼
Export.image.toDrive({image, description, ...})
```

### 今天踩过的坑

1. **`dataset is not defined`**
   - 原因：把 `var dataset = ...` 一起注释掉了
   - 学到的：Task05 中 dataset 创建部分必须保留，只注释 first() / Export / Map.addLayer

2. **误认为 `print(count)` 能把 ee.Number 变成 JavaScript Number**
   - 原因：看到 print 输出 28，以为已经转换
   - 纠正：print() 只是终端显示，真正转换需要 `evaluate()`

3. **`imageList[0]` 无法获取影像**
   - 原因：ee.List 不是 JavaScript Array
   - 纠正：必须用 `imageList.get(0)`

4. **两次 print 都输出 28，但对象类型不同**
   - 第一次：ee.Number（服务器对象）
   - 第二次：JavaScript Number（客户端数字）
   - 理解：值相同不代表类型相同

### 当前卡点

- 暂无（理论理解完成，下一步实际运行 28 景批量导出）

### 明天计划

- [ ] 在 GEE 中实际运行批量导出脚本，创建 28 个 Tasks
- [ ] 确认至少 5 个导出任务完成
- [ ] 开始下载 GeoTIFF 到本地 data/raw/
- [ ] 准备 Task 07：Python 批量读取 GeoTIFF 元数据
