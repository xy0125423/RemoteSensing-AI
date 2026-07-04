## 2026-07-01

- 初始化项目目录结构
- 完成 Python 开发环境配置
- 安装 rasterio、numpy、matplotlib
- 创建项目文档体系
- 创建数据目录
- 注册 Google Earth Engine（非商业项目）




## 2026-07-02

- 学会 Geometry 作为研究区域
- 学会 filterBounds()
- 学会 filterDate()
- 学会 filter() 云量过滤
- 成功完成 Sentinel-2 数据三层筛选
- 成功获得 28 张高质量影像


## 2026-07-03

- 学习 dataset.first()：ImageCollection → Image
- 学习 Map.addLayer() 可视化参数（bands/min/max）
- 理解 B2/B3/B4/B8 波段含义与用途
- 学习 Export.image.toDrive() 导出参数
- 解决 GEE 导出数据类型冲突 Bug（UInt16 vs Byte）
- 成功导出第一张 Sentinel-2 GeoTIFF（sentinel2_sample.tif）
- 将 GeoTIFF 放入 data/raw/sentinel2_sample.tif
- ✅ Task 01 & Task 02 完成


## 2026-07-04

- 安装 PyYAML，解决 import yaml 问题（安装名 ≠ 导入名）
- 学习 rasterio.open() 与 DatasetReader（Lazy Reading 工程思想）
- 学习 GeoTIFF Metadata：width、height、count、crs、transform、bounds
- 理解 Resolution 与真实面积换算（216×174 px × 100㎡ ≈ 3.76 km²）
- 理解 Band Mapping（dataset.read(1) = 导出第1个波段 = S2 B2）
- 理解 B4/B8 逐像素一一对应 → NDVI 计算基础
- 建立完整 GeoTIFF 数据流心智模型（文件 → DatasetReader → 二维数组 → 逐像素运算）
- ✅ Task 03 完成：read_geotiff.py 打印全部 GeoTIFF 元数据
- ✅ Task 04 完成：B4/B8 波段提取 + 统计信息（min/max/mean/std/shape/dtype）
- ✅ 新增 NDVI 首次计算：(b8 - b4) / (b8 + b4)，NumPy Element-wise Operation
- 新增 dtype 转换学习：uint16 → float32，遥感计算统一使用 float32
- 新增 ndarray / shape / Element-wise Op / NDVI / NIR / Reflectance 概念学习
- 踩坑 8 条 + 概念误区澄清 7 项


