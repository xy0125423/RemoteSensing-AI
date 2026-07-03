# RISK.md — 风险预判与避坑指南

> 本文档提前列出整个项目最容易踩的坑，并给出解决建议。  
> 每踩一个坑，在 NOTES.md 中记录，回到这里标注"已踩 ✅"。

---

## 风险等级说明

| 等级 | 含义 |
|------|------|
| 🔴 致命 | 可能导致几天甚至一周卡住 |
| 🟡 中度 | 会卡住几小时，但有解法 |
| 🟢 轻微 | 常见小坑，几分钟解决 |

---

## 1. GEE 相关风险

### 🔴 GEE Python API 认证失败

**现象**：`ee.Initialize()` 报错，终端提示认证问题。

**原因**：
- 未运行 `ee.Authenticate()`
- 认证令牌过期
- 网络代理/VPN 干扰认证流程

**解决**：
```python
# 首次或重新认证
import ee
ee.Authenticate()  # 会打开浏览器，登录 Google 账号
ee.Initialize(project='your-project-id')  # 需要 GEE 项目 ID
```

**预防**：
- 在项目开始阶段就完成认证
- 将认证状态检查写入 `check_env.py`
- 注意 GEE 现在需要关联 Google Cloud Project

---

### 🔴 GEE 导出任务一直不完成

**现象**：Export.image.toDrive() 任务在 Tasks 面板中长时间处于 RUNNING 状态。

**原因**：
- 导出区域太大 → 文件过大
- GEE 服务器排队
- 波段数太多
- scale 设置太小

**解决**：
- 缩小导出区域（先导小范围测试）
- 只 select 需要的波段（B2, B3, B4, B8）
- scale 设置为 10（Sentinel-2 原生分辨率），不要设更小
- 设置 `maxPixels: 1e9` 上限（默认可能不够）
- 如果超过 30 分钟，取消重建

**预防**：
- 第一次导出用最小的 Study Area
- 先只导出 1 景验证流程
- 设置合理的 maxPixels

---

### 🟡 GEE 数据集名称变更

**现象**：`ee.ImageCollection("COPERNICUS/S2")` 找不到数据集。

**原因**：GEE 偶尔会更新数据集 ID 或废弃旧版本。

**解决**：
- 在 GEE Code Editor 搜索栏中搜索 "Sentinel-2"
- 查看数据集文档确认最新 ID
- 当前使用的 ID：`"COPERNICUS/S2_SR_HARMONIZED"`（L2A 产品）

**预防**：
- DECISIONS.md 中记录使用的数据集 ID 和版本
- 定期检查 GEE 数据目录

---

### 🟡 GEE 计算超时

**现象**：GEE Code Editor 中代码运行超时（"Computation timed out"）。

**原因**：
- 计算量过大（区域大 + 时间长）
- 在 `map()` 中使用了复杂函数
- 试图在交互模式下处理过多数据

**解决**：
- 缩小研究区域（先用小范围验证）
- 减少时间范围
- 复杂计算用 Export 而非交互式显示
- 使用 `sample()` 而非全域统计

---

### 🟢 GEE JavaScript vs Python API 语法差异

**现象**：从 Code Editor (JS) 复制代码到 Python 中报错。

**原因**：GEE 的 JS API 和 Python API 语法有细微差异。

**解决**：
- JS：`filterBounds(geometry)`→ Python：`filterBounds(geometry)`（相同）
- JS：`filterDate('2025-01-01', '2025-12-31')`→ Python：相同
- JS：`Map.addLayer()`→ Python：需要 `geemap` 库或不用
- JS：函数定义 `function(img){}`→ Python：`lambda img: ...` 或 `def f(img):`

**预防**：本项目建议数据获取部分在 GEE Code Editor (JS) 中完成，后续处理在本地 Python 中完成。

---

## 2. GDAL / rasterio 相关风险

### 🔴 rasterio 安装失败（Windows）

**现象**：`pip install rasterio` 报错，提示 GDAL 相关错误。

**原因**：rasterio 依赖 GDAL 的 C 库，Windows 上没有预编译的二进制。

**解决（按优先级）**：
1. **推荐**：使用 conda：`conda install -c conda-forge rasterio`（conda 会自动处理 GDAL 依赖）
2. 从 Christoph Gohlke 的网站下载预编译 wheel：https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio
3. 使用 pip + 指定版本的 wheel：`pip install rasterio‑1.3.x‑cp3xx‑win_amd64.whl`

**预防**：
- 如果还没装 rasterio，优先用 conda 创建环境
- 如果 Python 环境已经建立，尝试 `pip install rasterio` 先看能否直接成功
- 记录所用 Python 版本和 rasterio 版本

---

### 🟡 rasterio 打开文件报错 "No such file or directory"

**现象**：`rasterio.open('data/raw/file.tif')` 报文件不存在。

**原因**：
- 相对路径是从当前工作目录（cwd）解析的，不是从脚本所在目录
- Windows 路径分隔符问题

**解决**：
- 使用绝对路径
- 或在脚本开头切换到项目根目录：
  ```python
  import os
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  ```
- 使用 `pathlib.Path` 处理路径

---

### 🟡 波段索引混淆（rasterio band 从 1 开始）

**现象**：想读取 B4 波段，读出来却是 B3 的数据。

**原因**：rasterio 的 band index 从 1 开始，不是 0。

**解决**：
```python
# 正确：band index 从 1 开始
b4 = src.read(1)  # 第一个波段（如果只 select 了 B4,B3,B2,B8，则这是 B4）
b8 = src.read(4)  # 第四个波段 = B8

# 更安全的方式：通过波段描述查找
descriptions = src.descriptions
# 找到 "B4" 在 descriptions 中的位置，index+1 就是 band number
```

---

### 🟢 坐标参考系（CRS）不匹配

**现象**：用 rasterio 读取的坐标和 GEE 中显示的不一致。

**原因**：GEE 默认使用 EPSG:4326（WGS84 经纬度），但导出的 GeoTIFF 可能使用 UTM 投影。

**解决**：
- 在 GEE 导出时指定 `crs: 'EPSG:4326'` 以保持经纬度坐标
- 或使用 `rasterio.warp.transform()` 进行重投影

---

### 🟢 影像显示全白或全黑

**现象**：matplotlib 显示 Sentinel-2 影像时一片白。

**原因**：Sentinel-2 L2A 数据反射率值范围 0~10000（缩放 10000），直接 imshow 会饱和。

**解决**：
```python
# 除以 10000 还原为真实反射率
rgb = rgb / 10000.0
# 再做 2%~98% clip
vmin, vmax = np.percentile(rgb, [2, 98])
rgb_clipped = np.clip((rgb - vmin) / (vmax - vmin), 0, 1)
plt.imshow(rgb_clipped)
```

---

## 3. NDVI 计算相关风险

### 🟡 NDVI 数组中出现 NaN 或 inf

**现象**：NDVI 计算结果有 NaN 或无穷大值。

**原因**：分母 NIR+Red=0（水体、阴影区），或原始数据有无效值。

**解决**：
```python
ndvi = np.where(
    (nir + red) != 0,
    (nir - red) / (nir + red),
    0  # 或 np.nan，取决于后续处理
)
```

---

### 🟢 NDVI 值不等于预期范围

**现象**：NDVI 值全部 > 10 或 < -5。

**原因**：忘记将 Sentinel-2 L2A 的反射率除以 10000。

**解决**：计算 NDVI 前，将 B4 和 B8 除以 10000.0。

---

## 4. 时间序列相关风险

### 🟡 时间序列采样点太少

**现象**：一年只有 10~15 个有效 NDVI 观测值，插值后曲线不平滑。

**原因**：
- 云量阈值设太严（<5%）
- 研究区多云多雨

**解决**：
- 适当放宽云量阈值（如 <30%）
- 使用 Sentinel-2 云概率波段（SCL）替代简单云量过滤
- 考虑使用 Sentinel-1（SAR，不受云影响）做补充（进阶方案）

---

### 🟡 插值后结果不合理

**现象**：线性插值在两个相距较远的点之间画了一条直线，但实际 NDVI 在这个时间段可能波动很大。

**原因**：线性插值假设两点之间均匀变化，不适合长空白期。

**解决**：
- 对于 >30 天的空白期，标记为"不可靠"而非插值
- 使用三次样条插值（`scipy.interpolate.CubicSpline`）可以获得更自然的曲线
- 使用 SG 滤波（Savitzky-Golay）作为更高级的平滑+插值方案

---

## 5. FFT 相关风险

### 🔴 频率轴解读错误

**现象**：用 `fftfreq` 得到的频率值不知道什么意思。

**原因**：FFT 的频率轴是归一化频率，需要乘以采样率才能得到实际频率。

**解决**：
```python
N = len(ndvi_series)
dt = 1  # 时间步长 = 1 天
freq = np.fft.rfftfreq(N, d=dt)  # 直接得到 1/天 为单位的频率
period = 1.0 / freq  # 周期 = 1/频率，单位：天
# 注意：freq[0] = 0 → period[0] = inf → 需要跳过
```

**最重要**：频率轴单位确认！确认！再确认！

---

### 🟡 直流分量（0 频率）淹没其他频率

**现象**：频谱图上 0 频率处有一个巨大的峰，其他频率几乎看不见。

**原因**：NDVI 均值不是 0，导致 DC 分量很大。

**解决**：
```python
ndvi_demeaned = ndvi_series - np.mean(ndvi_series)
fft_result = np.fft.rfft(ndvi_demeaned)
```

---

### 🟡 频谱泄漏导致峰值模糊

**现象**：主周期附近的频谱不是尖锐的峰，而是扩散的"山丘"。

**原因**：信号长度不是周期的整数倍 → 频谱泄漏。

**解决**：
- 对信号做加窗处理（Hanning 窗）：
  ```python
  window = np.hanning(len(ndvi_series))
  fft_result = np.fft.rfft(ndvi_series * window)
  ```
- 或接受一定程度的泄漏（对主周期识别影响不大）

---

### 🟢 频率分辨率不够

**现象**：想区分 180 天和 200 天的周期，但频谱上分不开。

**原因**：频率分辨率 Δf = 1/(N×Δt)，N 太小 → 分辨率太粗。

**解决**：
- 增大 N（尽量用一整年的数据 = 365 天）
- Δf = 1/365 ≈ 0.0027 天⁻¹ → 周期分辨率在 180 天附近约 90 天，不够区分 180 vs 200
- 现实是：一年的数据能可靠检测年周期（365天）和半年周期（182天），更精细的周期需要多年数据
- 接受这个限制，在报告中如实说明

---

## 6. PDF 生成相关风险

### 🔴 中文字体乱码

**现象**：PDF 中中文显示为方块 (□□□) 或乱码。

**原因**：fpdf2 默认字体不支持 CJK 字符。

**解决**：
1. 下载免费中文字体（思源黑体/Noto Sans SC）：https://github.com/notofonts/noto-cjk
2. 将 `.ttf` 或 `.otf` 文件放到 `data/fonts/`
3. 在 fpdf2 中注册：
   ```python
   from fpdf import FPDF
   pdf = FPDF()
   pdf.add_font('NotoSansSC', '', 'data/fonts/NotoSansSC-Regular.ttf', uni=True)
   pdf.set_font('NotoSansSC', '', 12)
   ```

**预防**：在 Task 28（PDF 封面）就解决中文字体问题，不要拖到最后。

---

### 🟡 图片在 PDF 中模糊

**现象**：插入的图表在 PDF 中不清晰。

**原因**：matplotlib 保存图片时 DPI 太低。

**解决**：
```python
plt.savefig('output.png', dpi=300, bbox_inches='tight')
```

---

### 🟡 PDF 文件过大

**现象**：生成的 PDF 超过 50 MB。

**原因**：嵌入了太多高 DPI 图片。

**解决**：
- 图表使用 150 dpi（打印也够清晰）
- 地图使用 200 dpi（需要看清细节）
- 对 PNG 做压缩：`plt.savefig('output.png', dpi=150, optimize=True)`

---

## 7. 通用工程风险

### 🟡 依赖版本冲突

**现象**：`pip install` 后某些包不兼容。

**解决**：
- 使用虚拟环境（已 ✅）
- 在 requirements.txt 中固定版本号：`numpy==1.26.0`
- 定期 `pip freeze > requirements_lock.txt`

---

### 🟡 数据文件被 Git 追踪导致仓库过大

**现象**：`data/raw/` 中的 GeoTIFF 被提交到 Git，仓库变成几个 GB。

**解决**：
- 确认 `.gitignore` 包含 `data/raw/` 和 `data/processed/` 和 `outputs/`
- 如果已经提交，使用 `git rm --cached` 移除
- 大型数据文件使用 Git LFS 或直接不纳入版本控制

**预防**：已配置 ✅

---

### 🟢 硬盘空间不足

**现象**：28 景 Sentinel-2 影像（每景约 200 MB）= 约 5.6 GB。

**解决**：
- 只保留当前需要的 5~10 景本地影像
- 其余保留在 Google Drive，按需下载
- 或用 GEE 云端计算，不下载全部影像

---

## 8. 考研相关的"踩坑"

### 🔴 只做项目不复习考研

**风险**：过度投入项目，挤占考研复习时间。

**建议**：
- 严格按每天 3 小时执行
- 如果某天考研复习任务重，项目暂停一天（在 TASK_ROADMAP 中标注）
- Phase 4（FFT）天然与 892 重合，此阶段可以适当增加投入

---

### 🟡 复试时被追问深度学习

**风险**：导师问"为什么不用深度学习"，回答不好会被认为技术落后。

**准备答案**：
1. "本项目聚焦传统遥感方法，在有限数据条件下，NDVI + FFT 比 CNN 更稳健"
2. "本科阶段的重点是掌握遥感物理基础，这比调参更重要"
3. "本项目为后续引入深度学习方法（如 Sentinel-2 + LSTM 时序预测）打好了数据流水线基础"
4. "我的信号与系统基础（892）在本项目的 FFT 分析中得到了直接应用"

---

## 风险热力图

```
                   影响程度
               低      中      高
发生率  高   🟢     🟡      🔴
        中   🟢     🟡      🔴  ← GEE认证、中文字体
        低   🟢     🟡      🔴  ← rasterio安装(Win)
```

---

## 已踩坑记录

> 每踩一个坑，在这里记录日期和简要描述。这会成为未来的宝贵经验。

| 日期 | 风险编号 | 描述 | 解决方案 |
|------|----------|------|----------|
| 07-02 | GEE-JS | ImageCollection 拼写错误、lt 写成 1t | 仔细检查拼写，阅读报错信息 |
| — | — | — | — |
