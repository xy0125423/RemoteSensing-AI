# report_design.md — PDF 报告结构设计

> 定义最终 PDF 报告的内容结构、排版规范和数据来源。

---

## 报告章节

| 章节 | 页码 | 内容描述 | 数据来源 |
|------|------|---------|---------|
| 1. 封面 | p1 | 区域名 + 卫星影像时间范围 + 生成日期 | `config.yaml` |
| 2. 摘要 | p2 | 3-4 个 KPI 数字卡片（年均 NDVI、振幅、主周期、云覆盖率） | `ndvi_calc.py` + `fft_analyzer.py` |
| 3. 研究区域 | p3 | 区域地图 + 行政边界 + 表格（经纬度范围、面积） | `geocode.py` |
| 4. NDVI 空间分布 | p4 | 多时相 NDVI 地图（春夏秋冬四宫格） | `visualizer.py` → `outputs/maps/` |
| 5. NDVI 时间序列 | p5 | 全年 NDVI 折线图（原始值 + 平滑值） | `visualizer.py` → `outputs/charts/` |
| 6. FFT 频谱分析 | p6 | 频谱图 + 主周期表格 | `visualizer.py` → `outputs/charts/` |
| 7. 方法说明 | p7 | 数据源、处理流程、公式 | 静态内容 |

---

## 排版规范

- 页面尺寸: A4 (210 × 297 mm)
- 正文字体: 宋体 (SimSun) 10pt
- 标题字体: 黑体 (SimHei)
  - 一级标题: 18pt 加粗
  - 二级标题: 14pt 加粗
- 配色:
  - 主色: #2c7bb6 (蓝)
  - 强调色: #d7191c (红)
  - NDVI 正值: #1a9850 (绿)
  - NDVI 零值: #ffffbf (黄)
- 页边距: 上下 2cm，左右 2.5cm
- 页脚: 居中页码

---

## KPI 数字卡片

| 指标 | 计算方式 | 单位 |
|------|---------|------|
| 年均 NDVI | `ndvi_series.mean()` | 无因次 |
| 年内振幅 | `ndvi_max - ndvi_min` | 无因次 |
| 主周期 | FFT 振幅最大的周期 | 天 |
| 生长季长度 | NDVI > 0.3 的连续天数 | 天 |

---

## 技术栈

- `reportlab` — PDF 排版引擎
- `Pillow` — 图片嵌入
- `matplotlib` — 地图和图表渲染
