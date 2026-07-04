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

- [ ] 使用 matplotlib 显示 Sentinel-2 真彩色影像（B4-B3-B2）
- [ ] 对数据进行 2%~98% 拉伸（clip），增强对比度
- [ ] 尝试使用 rasterio 的 transform 设置正确的坐标轴

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
