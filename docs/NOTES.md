# 学习笔记

## 2026-07-01

### 什么是 GeoTIFF？

GeoTIFF 是一种带有地理坐标信息的 TIFF 文件。

它不仅保存影像像素，还保存：

- 坐标系（CRS）
- 地理范围（Bounds）
- 仿射变换（Transform）
- 波段（Bands）

普通 JPG 只能表示图片，而 GeoTIFF 可以表示真实地球上的位置，因此广泛应用于遥感和 GIS。、

### Sentinel-2 波段

虽然 Sentinel-2 常说有 13 个光谱波段，但在 GEE 中的数据产品还包含质量控制和辅助波段，因此实际看到的 Bands 数量可能更多（如 26 个）。

目前最重要的波段：

- B2：蓝光（Blue）
- B3：绿光（Green）
- B4：红光（Red）
- B8：近红外（Near Infrared）

真彩色显示通常使用：

B4 + B3 + B2



### 什么是 ImageCollection？

ImageCollection 是 GEE 中用于存放大量遥感影像的集合。

例如 Sentinel-2 数据集不是一张图片，而是由全球不同地区、不同时间获取的大量影像组成。

在 GEE 中，我们通常先获取 ImageCollection，再筛选区域、时间和云量，最后得到需要分析的一张或多张影像。


## 今天我学会了什么？

今天真正接触了 Google Earth Engine（GEE）。

以前我一直以为做遥感就是先下载数据，再用电脑处理。

今天才知道不是。

GEE 更像是 Google 提供的一个遥感数据库和超级计算机。

我的电脑不是在计算，而是在告诉 Google："帮我找数据，帮我计算。"

另外，我也知道了：

GeoTIFF 不是普通图片。

它除了图片本身，还记录了坐标、波段等信息，每一个像素都对应地球上的真实位置。

我还知道了 Sentinel-2 不是只有 RGB，而是有很多波段，以后 NDVI 就要用其中的 B4 和 B8。

最重要的是，我第一次真正把 Sentinel-2 遥感影像显示到了地图上。

## 今天最让我意外的是什么？

有两件事。

第一件。

我一直以为 GEE 会把数据下载到我的电脑。

结果发现，它其实是在 Google 的服务器上处理数据，我只是发送命令。

第二件。

我以为一张遥感图片就是一张图片。

结果发现它居然有二十多个波段，而且每个像素都有自己的地理坐标。

感觉它更像一份科学数据，而不是照片。

## 我还有什么没理解？

1.

ImageCollection 和 Image 到底是什么关系？

我知道一个是影像集合，一个是一张影像。

但是以后什么时候该用 Collection，什么时候该用 Image，还需要继续学习。
1. ImageCollection 和 Image 的关系

你的理解没错，但关键是使用场景：

· Image：处理单张影像，比如筛选出某一天的一景，做波段计算、裁剪。
· ImageCollection：处理时间序列或批量影像，比如计算某地区整个夏天的NDVI最大值、做月合成、去云批处理。

核心区别：Collection 可以 .map() 批量处理每一张 Image，也可以 .reduce() 把多张合成一张（比如中值合成）。以后养成习惯：先 Filter 成 Collection，再缩小范围取出单张 Image。

---


2.

为什么 Sentinel-2 有 26 个波段？

我知道以后只会经常用 B2、B3、B4、B8。

但是其他波段到底是干什么的，还不理解。

2. Sentinel-2 为什么有 26 个波段

S2 携带多光谱仪器（MSI），26个波段包括：

· 10米：B2（蓝）、B3（绿）、B4（红）、B8（近红外）——你常用的
· 20米：B5~B7（红边）、B8A（窄近红外）、B11~B12（短波红外）——用于植被健康、含水量
· 60米：B1（气溶胶）、B9（水汽）、B10（卷云）——用于大气校正

其他波段的用途：红边波段（B5~B7）是植被胁迫监测的利器，短波红外（B11~B12）用于火烧迹地、土壤湿度。但新手阶段，专注 B2/B3/B4/B8 完全够用。

---


3.

GEE 到底是怎么下载数据到本地的？

今天只是显示到了地图上。

后面是怎么变成电脑里的 GeoTIFF 文件的，我还不知道。
3. GEE 怎么下载到本地

GEE 本身是云端平台，不直接“下载”，而是导出：

· 使用 Export.image.toDrive() 导出到你的 Google Drive
· 或 Export.image.toAsset() 存回 GEE 的 Asset
· 然后从 Google Drive 下载 GeoTIFF 到电脑

关键点：导出是异步任务，在右侧 Tasks 选项卡里点击“Run”才会真正执行。不能像本地文件那样 save()。

---

4.

Map.addLayer() 到底做了什么？

为什么写几行代码，地图上就突然出现了遥感影像？
4. Map.addLayer() 到底做了什么

它是前端可视化方法，做了三件事：

1. 把你的影像数据从 GEE 服务器拉取缩略图（不是完整数据）
2. 根据你指定的 visParams（波段组合、拉伸范围）动态渲染成彩色图片
3. 把这张图片叠加在 Code Editor 的地图底图上

所以它只显示，不下载，显示的是经过拉伸的“好看”版本，不是原始DN值。你写的代码是在服务器端构建指令，Map.addLayer 是发请求让服务器“画一张图发回来”。

---
总结一句话：

· Collection 是“批量处理”，Image 是“单张操作”
· 多余波段留着以后用，新手先用可见光+近红外
· 下载靠 Export，不是靠显示
· Map.addLayer 是“看图”指令，不是“取数”指令


## 今天最大的收获

今天是这个项目真正开始的第一天。

虽然只是写了几行代码，但是这是我第一次真正接触遥感开发，而不是看别人演示。

我发现自己并不是完全不会。

很多东西，只要一步一步理解，其实没有想象中那么难。

希望以后继续保持今天这种学习方式，不追求快，而是真正理解每一步。




## 2026-07-02

## 学习Geometry

Geometry 表示研究区域。

它可以是：

- Point
- Line
- Polygon
- Rectangle

Google Earth Engine 真正识别的是 Geometry，
不是行政区名称。

---

## ImageCollection

ImageCollection 是影像集合。

经过：

- filterBounds()
- filterDate()
- filter()

之后，

仍然是 ImageCollection。

只有后续选择具体影像后，
才会变成 Image。

---

## Cloud Filter

Sentinel-2 自带属性：

CLOUDY_PIXEL_PERCENTAGE

常见写法：

ee.Filter.lt(
    "CLOUDY_PIXEL_PERCENTAGE",
    10
)

表示：

保留云量小于10%的影像。
2026-07-02

今天不是简单学了三个 API。

而是真正建立了遥感数据获取的工程思维。

第一次理解：

遥感数据不是下载下来直接计算。

而是：

空间筛选

↓

时间筛选

↓

质量筛选

↓

得到真正可分析的数据。

这是整个 RemoteSensing-AI 项目第一次形成完整的数据筛选流水线。

最终：

从全球 Sentinel-2 数据集中，

成功筛选出研究区域内，

2025 年云量小于10%的

28 张高质量影像。

这是整个项目迈出的第一步，也是后续 NDVI、时序分析、FFT、PDF 自动生成等所有功能的数据基础。


## 2026-07-03

### ImageCollection → Image

`dataset.first()` 从集合中取出第一张影像。

- `filter()` 不会排序
- `first()` 不代表云量最小，仅表示当前集合中的第一张

### Map.addLayer() 真正用法

不能直接 `Map.addLayer(image)`，地图会变黑。

必须指定可视化参数：

```javascript
Map.addLayer(image, {
    bands: ["B4", "B3", "B2"],
    min: 0,
    max: 3000
}, "True Color");
```

三个参数：
1. 要显示的 Image
2. 可视化参数（波段组合 + 拉伸范围）
3. 图层名称

### B2/B3/B4/B8 速记

| 波段 | 颜色 | 用途 |
|------|------|------|
| B2 | Blue | 真彩色 |
| B3 | Green | 真彩色 |
| B4 | Red | 真彩色 + NDVI |
| B8 | Near Infrared | NDVI |

真彩色 = B4 + B3 + B2
NDVI = (B8 - B4) / (B8 + B4)

### Export.image.toDrive() 参数

```javascript
Export.image.toDrive({
    image: exportImage,       // 要导出的 Image
    description: 'Task名称',  // Tasks 面板显示的名称
    folder: 'GEE_Exports',    // Google Drive 文件夹
    fileNamePrefix: '文件名',  // 最终文件名
    region: geometry,         // 导出区域（必须用 geometry！）
    scale: 10,                // 分辨率 10m（Sentinel-2 可见光）
    maxPixels: 1e13           // 最大像素数
});
```

### 关键工程经验

1. **不要导出全部波段**：Sentinel-2 不同波段有不同数据类型（UInt16 / Byte），混在一起导出会报错。用 `select()` 只选需要导出的波段。
2. **GEE 先保存再运行**：Ctrl+S → Run，养成肌肉记忆，否则刷新页面代码全丢。
3. **JavaScript 对象逗号**：每个属性后面必须有逗号，最后一个属性可省略。


## 2026-07-04

### Python 库安装名 vs 导入名

安装名和导入名有时不同，这是 Python 生态的常见现象：

| 安装名 | 导入名 |
|--------|--------|
| pyyaml | yaml |
| opencv-python | cv2 |
| pillow | PIL |
| scikit-learn | sklearn |

以后安装后报黄色波浪线，先确认这两者是否一致。

### rasterio.open() 与 DatasetReader

```python
import rasterio
dataset = rasterio.open('sentinel2_sample.tif')
```

返回的是 `DatasetReader`——一个读取器，不是数据本身。

核心工程思想：**Lazy Reading（按需读取）**。

GeoTIFF 不一次性加载到内存，需要哪个波段就读哪个，避免大型遥感数据撑爆内存。

### GeoTIFF 元数据速查

| 属性 | 含义 | 单位 |
|------|------|------|
| dataset.width | 图像宽度 | 像素 |
| dataset.height | 图像高度 | 像素 |
| dataset.count | 波段数量 | 个 |
| dataset.crs | 坐标参考系 | EPSG |
| dataset.transform | 仿射变换 | — |
| dataset.bounds | 地理范围 | 经纬度 |

### Resolution（分辨率）

10m Resolution 意味着：

一个 Pixel = 10m × 10m = 100㎡

真实宽度 = width × Resolution
真实高度 = height × Resolution

当前 GeoTIFF：216 × 174 像素 × 100㎡ = 3758400㎡ ≈ 3.76 km²

### Band Mapping（波段映射关系）

导出的 GeoTIFF 只包含 4 个波段，数据集内部重新编号：

| dataset.read() | 导出文件中的位置 | 原始 Sentinel-2 波段 |
|---------------|-----------------|---------------------|
| read(1) | 第 1 个波段 | B2（Blue） |
| read(2) | 第 2 个波段 | B3（Green） |
| read(3) | 第 3 个波段 | B4（Red） |
| read(4) | 第 4 个波段 | B8（NIR） |

**关键理解**：`dataset.read(1)` 读取的是导出顺序的第 1 个，不是 Sentinel-2 原始 Band 1。

### 为什么 B4 和 B8 能算 NDVI

四个波段拍的是同一块区域、同一时刻。

B4 和 B8 的每个 Pixel 位置一一对应。

区别仅仅是：不同光谱波段对同一地面的不同响应。

所以公式 NDVI = (B8 - B4) / (B8 + B4) 是逐像素一一对应的数学运算。

### GeoTIFF vs JPG

| 特性 | JPG | GeoTIFF |
|------|-----|---------|
| 坐标信息 | ❌ | ✅（CRS + Transform） |
| 多波段 | ❌（RGB 三通道） | ✅（任意波段数） |
| 数据类型 | 8-bit 整数 | uint16 / float32 |
| 用途 | 看图 | 科学分析 |

### dataset.read() 返回值

`dataset.read(1)` 返回的是一个**二维 numpy 数组**（整个波段的所有像素），不是单个数值。

- 形状：`(height, width)`，例如 `(174, 216)`
- 类型：取决于 GeoTIFF 存储类型（Sentinel-2 L2A 通常是 uint16）
- 取单个像素：`data[row, col]`

### VS Code 生产力技巧

| 现象 | 含义 | 该怎么做 |
|------|------|----------|
| 文件 tab 黄色数字 | Problems 面板有 Warning | 点开查看具体提示，不一定是错误 |
| import 黄色波浪线 | Pylance 找不到模块 | `pip show <包名>` 确认是否已安装 |
| 终端无输出 | 代码没有 print() | 程序可能已成功执行，加 print 验证 |
| 程序是否成功 | 看 Terminal 不是编辑器 | 终端返回码为 0 = 成功 |

### 今日踩坑总结

今天建立的认知：**遥感工程开发不是 API 背诵，而是数据结构理解**。

核心心智模型：
```
GeoTIFF 文件 ──rasterio.open()──▶ DatasetReader（读取器）
                                     │
                                     ├── .width / .height（像素数量，不是米）
                                     ├── .count（导出波段数，不是 S2 原始编号）
                                     ├── .crs / .transform（地理坐标信息）
                                     └── .read(i)（第 i 个波段的二维数组）
```

后续所有操作（NDVI、NDWI、EVI、时序分析）都建立在这个模型之上。

---

### NumPy ndarray — 遥感数据的载体

`dataset.read()` 返回的是 `numpy.ndarray`，不是 Python 原生的 list。

```python
b4 = dataset.read(3)          # 返回 numpy.ndarray
print(type(b4))               # <class 'numpy.ndarray'>
print(b4.shape)               # (174, 216) — 174 行 × 216 列
print(b4.dtype)               # uint16 — 原始数据类型
```

**ndarray vs Python list**：

| 特性 | Python list | numpy.ndarray |
|------|-------------|---------------|
| 存储 | 分散在内存中 | 连续内存块 |
| 运算 | 需要 for 循环 | 向量化，一次处理全部 |
| 数学操作 | `[x+1 for x in lst]` | `arr + 1` |
| 科学计算 | 不适合 | 专为科学计算设计 |

**为什么遥感必须用 ndarray**：一张 Sentinel-2 影像 216×174 = 37,584 个像素。用 Python for 循环一个个算 NDVI 会极慢；用 ndarray 的 Element-wise Operation 一次性完成。

---

### shape — 数组的维度信息

```python
b4.shape    # (174, 216)
ndvi.shape  # (174, 216) — NDVI 和原始波段同形状
```

- `(174, 216)` = (行数, 列数) = (height, width)
- 每个波段 shape 完全相同，所以可以逐像素运算

---

### dtype — 数据类型

| dtype | 范围 | 内存 | 用途 |
|-------|------|------|------|
| uint16 | 0 ~ 65535 | 2 字节 | Sentinel-2 原始存储 |
| float32 | ±3.4×10³⁸ | 4 字节 | NDVI 等浮点运算 |

**关键操作**：
```python
b4 = dataset.read(3)              # dtype = uint16
b4 = b4.astype('float32')         # dtype = float32
```

**为什么必须转换**：
- uint16 的除法：`5 / 2 = 2`（整数除法，丢失小数）
- float32 的除法：`5.0 / 2.0 = 2.5`（保留小数）
- NDVI 值在 -1~1 之间，必须用浮点类型

---

### uint16 — 遥感数据的整数存储格式

Sentinel-2 L2A 产品将地表反射率（0~1）乘以 10000 后存储为 uint16 整数。

```
DN 值  = 地表反射率 × 10000
例如：DN = 3500  →  真实反射率 = 0.35
```

**为什么这样做**：整数存储比浮点数更省空间（2 字节 vs 4 字节），且无损精度。

---

### float32 — 科学计算的标准浮点类型

```python
b4 = b4.astype('float32')  # 转换后可以进行浮点除法
```

选择 float32 而非 float64 的原因：
- float32 精度足够（7 位有效数字），NDVI 只需要 2~3 位
- 内存减半（4 字节 vs 8 字节）
- 本项目 216×174=37,584 像素，float32 完全可以

---

### Reflectance（地表反射率）

地表反射率 = 地面反射的辐射 / 到达地面的辐射，范围 0~1。

- Sentinel-2 L2A 已做大气校正，数据即地表反射率
- DN ÷ 10000 = 真实反射率
- 例如：B4 的 DN 均值 1500 → 反射率 0.15（红光波段低反射，植被吸收了红光）

---

### Pixel（像素）

一个 Pixel = 遥感影像的最小单元 = 地面上 10m×10m 的正方形区域。

本张影像：216 × 174 = 37,584 个像素，每个像素在 B4 和 B8 中位置一一对应。

---

### NIR（近红外，Near Infrared）

Sentinel-2 Band 8，波长约 785~899 nm，人眼不可见。

- 健康植被在 NIR 波段**强反射**（细胞结构散射）
- 裸土/建筑在 NIR 波段反射较弱
- NDVI 的核心原理：利用 NIR 与 Red 的反射差异检测植被

---

### Element-wise Operation（逐元素运算）

NumPy 的核心特性：一次运算作用于整个数组的每个元素。

```python
ndvi = (b8 - b4) / (b8 + b4)
```

这条语句等价于对 37,584 个像素各执行一次 NDVI 公式，**无需 for 循环**。

| 写法 | 执行方式 | 速度 |
|------|----------|------|
| `for i in range(174): for j in range(216): ndvi[i][j] = (b8[i][j] - b4[i][j]) / (b8[i][j] + b4[i][j])` | Python 逐像素循环 | 很慢 |
| `ndvi = (b8 - b4) / (b8 + b4)` | NumPy C 层向量化 | 极快 |

**这是 Python 遥感数据处理的核心工程范式。**

---

### NDVI（归一化植被指数）

```
NDVI = (NIR - Red) / (NIR + Red)
     = (B8 - B4) / (B8 + B4)
```

| NDVI 值 | 含义 |
|---------|------|
| 0.6 ~ 1.0 | 茂密健康植被 |
| 0.3 ~ 0.6 | 稀疏植被 / 草地 |
| 0.0 ~ 0.3 | 裸土 / 建筑 |
| -1.0 ~ 0.0 | 水体 / 云 / 阴影 |

**为什么公式有效**：
- 红光（B4）：植被吸收红光（光合作用）→ 反射低
- 近红外（B8）：植被散射近红外（细胞结构）→ 反射高
- 差值越大 → 植被越健康

**本项目实测结果**（基于 `read_geotiff.py` 运行输出）：
- NDVI min / max / mean / std → 所有像素一次性计算完成
- shape = (174, 216)，dtype = float32

### CRS（Coordinate Reference System，坐标参考系）

定义影像如何映射到地球表面。

```python
dataset.crs  # 例如 EPSG:32650（WGS 84 / UTM zone 50N）
```

EPSG 编码是全球统一的坐标系统编号。UTM（Universal Transverse Mercator）是常用的投影坐标系，单位是米。

### Bounds（地理范围）

影像四个角的经纬度坐标。

```python
dataset.bounds  # BoundingBox(left=..., bottom=..., right=..., top=...)
```

格式：`(左, 下, 右, 上)` = `(min_lon, min_lat, max_lon, max_lat)`

### Transform（仿射变换）

6 个参数描述如何从 (row, col) 像素坐标转换为地理坐标。

```python
dataset.transform  # Affine(a, b, c, d, e, f)
```

| 参数 | 含义 |
|------|------|
| a | 像素宽度（通常 = Resolution） |
| e | 像素高度（通常 = -Resolution，负值表示北在上） |
| c, f | 左上角像素的坐标 |