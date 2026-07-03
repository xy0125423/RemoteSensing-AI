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
- [x] 获取第一张 Sentinel-2 GeoTIFF
- [×] 使用 rasterio 读取 GeoTIFF 元数据



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

- [ ] 使用 rasterio 读取 sentinel2_sample.tif 并打印元数据
- [ ] 提取 B4 和 B8 波段为 numpy 数组
- [ ] 使用 matplotlib 显示真彩色影像
