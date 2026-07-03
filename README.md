# RemoteSensing-AI

> 基于 Google Earth Engine + Sentinel-2 的 NDVI 时间序列分析工具
>
> 输入地名 → 自动获取卫星影像 → 计算 NDVI → FFT 频谱分析 → 生成 PDF 报告

---

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. GEE 认证（首次使用）
earthengine authenticate

# 3. 运行分析
python main.py --region 郓城县
```

---

## 功能

- 🌍 **地名→坐标**: 支持中国省/市/县级区域名称
- 🛰️ **GEE 数据获取**: Sentinel-2 Level-2A 多光谱影像
- 🌿 **NDVI 计算**: 归一化植被指数 + 去云掩膜
- 📈 **时间序列分析**: 插值 + 平滑 + 季节分解
- 🔢 **FFT 频谱**: 识别植被周期模式
- 📊 **可视化**: NDVI 地图 + 时序图 + 频谱图
- 📄 **PDF 报告**: 一键生成专业分析报告

---

## 项目结构

详见 [blueprint/PROJECT_ARCHITECTURE.md](blueprint/PROJECT_ARCHITECTURE.md)

---

## 依赖

- Python 3.10+
- Google Earth Engine API
- NumPy, SciPy, Pandas
- Matplotlib, ReportLab
- GeoPandas, Rasterio

---

## 进度

- [ ] GEE 数据获取
- [ ] NDVI 批量计算
- [ ] FFT 频谱分析
- [ ] 可视化
- [ ] PDF 报告生成
