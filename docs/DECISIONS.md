## 2026-07-01：提前完成 Google Earth Engine 配置

- 原计划：第二战开始配置 GEE
- 最终决定：项目初始化阶段完成 GEE 注册
- 原因：
  - 后续所有遥感数据统一来自 GEE
  - 避免后续开发时中断去配置环境
  - 保持整个项目的数据来源一致



## 2026-07-02

整个项目采用逐层筛选的数据流：

ImageCollection

↓

filterBounds()

↓

filterDate()

↓

Cloud Filter

↓

ImageCollection

↓

Image

而不是直接使用 dataset.first()。

原因：

先保证数据质量，再进入后续分析。

---

研究阶段使用较小 Study Area。

原因：

- 运算更快
- 更容易观察结果
- 更适合学习 Rasterio 与 NDVI


## 2026-07-03：GEE 导出只保留必要波段

- 问题：导出全部波段导致数据类型冲突（UInt16 vs Byte）
- 决定：使用 select(['B2','B3','B4','B8']) 只导出需要的波段
- 原因：
  - 避免数据类型不兼容
  - 减小文件体积
  - 后续分析只需要这 4 个波段
- 原则：工程开发不导出多余数据，按需取用