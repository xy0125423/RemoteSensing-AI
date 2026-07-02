# 今日任务

## 当前阶段26年7月1日
一战：GeoTIFF 驯服战

## 今天完成
- [x] 创建项目目录
- [x] 创建文档体系（README、PROJECT、TODAY、DECISIONS、CHANGELOG）
- [x] 创建 Python 虚拟环境
- [x] 安装 numpy、matplotlib、rasterio
- [x] 验证 Python 开发环境（check_env.py）
- [x] 创建 data/raw、data/processed、outputs、scripts 目录
- [x] 注册 Google Earth Engine（非商业项目）

## 当前卡点
- 暂无

## 明天计划
- [ ] 学习 GeoTIFF 基础概念
- [ ] 获取第一张 Sentinel-2 GeoTIFF
- [ ] 使用 rasterio 读取 GeoTIFF 元数据


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