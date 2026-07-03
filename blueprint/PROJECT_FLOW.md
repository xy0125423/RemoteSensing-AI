# PROJECT_FLOW — 项目流程图

> 使用 Mermaid 语法绘制，GitHub 和 VS Code 可直接渲染预览。

---

## 1. 系统总体流程（用户视角）

```mermaid
flowchart TD
    A["👤 用户输入<br/>地名/坐标"] --> B["🌍 地名解析<br/>地名 → 经纬度"]
    B --> C["🛰️ GEE 数据获取<br/>Sentinel-2 ImageCollection"]
    C --> D{"☁️ 云量过滤<br/>CLOUDY_PIXEL_PERCENTAGE < 10%"}
    D -->|通过| E["📦 筛选后影像集<br/>(N 景高质量影像)"]
    D -->|不通过| C
    
    E --> F["🌿 NDVI 计算<br/>NDVI = (NIR-Red)/(NIR+Red)"]
    F --> G["📊 时间序列构建<br/>(日期, NDVI均值)"]
    
    G --> H["🔍 数据清洗<br/>异常值检测 + 插值 + 平滑"]
    H --> I["📈 物候指标提取<br/>峰值日期、生长季起止"]
    
    H --> J["🔢 傅里叶分析<br/>scipy.fft.rfft()"]
    J --> K["📉 频谱图<br/>主周期提取"]
    
    I --> L["🎨 可视化模块<br/>地图 + 折线图 + 频谱图"]
    K --> L
    
    L --> M["📄 PDF 报告生成<br/>fpdf2 自动排版"]
    M --> N["✅ 最终输出<br/>PDF 分析报告"]
```

---

## 2. 技术实现流程（开发者视角）

```mermaid
flowchart TD
    subgraph Phase1["Phase 1: GeoTIFF 驯服战"]
        P1A["GEE Export.image.toDrive()"] --> P1B["Google Drive 下载"]
        P1B --> P1C["rasterio 读取元数据"]
        P1C --> P1D["numpy 波段提取"]
        P1D --> P1E["matplotlib 真彩色显示"]
    end
    
    subgraph Phase2["Phase 2: NDVI 计算引擎"]
        P2A["NDVI 公式理解"] --> P2B["numpy 向量化计算"]
        P2B --> P2C["NDVI GeoTIFF 写入"]
        P2C --> P2D["NDVI 伪彩色图"]
        P2D --> P2E["批量 NDVI → CSV"]
    end
    
    subgraph Phase3["Phase 3: 时间序列分析"]
        P3A["读取 NDVI CSV"] --> P3B["异常值检测 (MAD)"]
        P3B --> P3C["线性插值 (均匀采样)"]
        P3C --> P3D["滑动平均平滑"]
        P3D --> P3E["物候指标提取"]
    end
    
    subgraph Phase4["Phase 4: 傅里叶分析"]
        P4A["FFT 基础验证"] --> P4B["NDVI rfft()"]
        P4B --> P4C["幅度谱 + 功率谱"]
        P4C --> P4D["主周期提取"]
        P4D --> P4E["频谱解读笔记"]
    end
    
    subgraph Phase5["Phase 5: 可视化与报告"]
        P5A["报告结构设计"] --> P5B["fpdf2 封面"]
        P5B --> P5C["地图可视化"]
        P5C --> P5D["时序图美化"]
        P5D --> P5E["频谱图美化"]
        P5E --> P5F["完整 PDF 生成"]
    end
    
    subgraph Phase6["Phase 6: 系统集成"]
        P6A["地名→坐标"] --> P6B["config.yaml"]
        P6B --> P6C["pipeline.py"]
        P6C --> P6D["logging 日志"]
        P6D --> P6E["测试脚本"]
        P6E --> P6F["3 份示例报告"]
    end
    
    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Phase5
    Phase5 --> Phase6
```

---

## 3. 数据流转图

```mermaid
flowchart LR
    subgraph Input["输入"]
        A1["地名<br/>郓城县"]
    end
    
    subgraph Cloud["GEE 云端"]
        B1["Sentinel-2<br/>ImageCollection"]
        B2["filterBounds<br/>filterDate<br/>Cloud Filter"]
        B3["NDVI .map()<br/>云端计算"]
    end
    
    subgraph Local["本地处理"]
        C1["GeoTIFF<br/>data/raw/"]
        C2["NDVI 数组<br/>numpy"]
        C3["ndvi_series.csv<br/>data/processed/"]
        C4["插值序列<br/>均匀采样"]
        C5["FFT 频谱<br/>scipy"]
        C6["物候指标<br/>JSON"]
    end
    
    subgraph Output["输出"]
        D1["地图<br/>PNG 300dpi"]
        D2["折线图<br/>PNG 300dpi"]
        D3["频谱图<br/>PNG 300dpi"]
        D4["PDF 报告<br/>outputs/"]
    end
    
    A1 --> B1
    B1 --> B2
    B2 -->|"Export"| C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    C3 --> C6
    C4 --> C5
    
    C2 --> D1
    C3 --> D2
    C5 --> D3
    
    D1 --> D4
    D2 --> D4
    D3 --> D4
    C6 --> D4
```

---

## 4. 模块依赖关系图

```mermaid
flowchart TD
    main.py["main.py<br/>流程编排"] --> geocode["geocode.py<br/>地名解析"]
    main.py --> gee_fetcher["gee_fetcher.py<br/>GEE 数据获取"]
    main.py --> ndvi_calc["ndvi_calc.py<br/>NDVI 计算"]
    main.py --> timeseries["timeseries.py<br/>时间序列"]
    main.py --> fft_analyzer["fft_analyzer.py<br/>FFT 分析"]
    main.py --> visualizer["visualizer.py<br/>可视化"]
    main.py --> report_gen["report_gen.py<br/>PDF 生成"]
    main.py --> config["config.py<br/>配置加载"]
    
    gee_fetcher --> geocode
    ndvi_calc --> gee_fetcher
    timeseries --> ndvi_calc
    fft_analyzer --> timeseries
    visualizer --> ndvi_calc
    visualizer --> timeseries
    visualizer --> fft_analyzer
    report_gen --> visualizer
    report_gen --> timeseries
    
    config -.-> gee_fetcher
    config -.-> ndvi_calc
    config -.-> timeseries
    config -.-> fft_analyzer
    config -.-> visualizer
    config -.-> report_gen
```

---

## 5. 每个 Task 的决策树（以 NDVI 计算为例）

```mermaid
flowchart TD
    Start["开始 NDVI 计算"] --> Q1{"数据来源？"}
    Q1 -->|"GEE 云端"| G1["在 GEE 中 .map()<br/>计算 NDVI"]
    Q1 -->|"本地 GeoTIFF"| G2["rasterio 读取<br/>B4, B8 波段"]
    
    G1 --> Q2{"需要导出到本地？"}
    Q2 -->|是| G1A["Export NDVI 波段<br/>到 Drive"]
    Q2 -->|否| G1B["直接在 GEE 中<br/>提取时序"]
    
    G2 --> G2A["numpy 向量化<br/>ndvi = (nir-red)/(nir+red)"]
    G2A --> G2B["处理除零<br/>np.where"]
    G2B --> G2C["写入 NDVI GeoTIFF"]
    
    G1A --> G3["下载 NDVI GeoTIFF"]
    G3 --> G2A
    
    G1B --> G4["ui.Chart 画时序图"]
    G2C --> End1["输出: NDVI GeoTIFF"]
    G4 --> End2["输出: GEE 时序图"]
```

---

## 6. 最终 PDF 报告结构

```mermaid
flowchart TD
    Cover["📔 封面<br/>标题 + 作者 + 日期"] --> TOC["📑 目录"]
    TOC --> Ch1["第1章 研究区概况<br/>位置地图 + 基本信息"]
    Ch1 --> Ch2["第2章 数据来源与方法<br/>Sentinel-2 + NDVI 公式"]
    Ch2 --> Ch3["第3章 NDVI 空间分析<br/>真彩色图 + NDVI 伪彩色图"]
    Ch3 --> Ch4["第4章 NDVI 时间序列<br/>折线图 + 物候指标表"]
    Ch4 --> Ch5["第5章 频谱分析<br/>FFT 频谱图 + 主周期表"]
    Ch5 --> Ch6["第6章 结论与讨论<br/>总结 + 局限性 + 展望"]
    Ch6 --> Appendix["附录<br/>代码说明 + 参考文献"]
```

---

## 7. 考研知识关联流程

```mermaid
flowchart LR
    subgraph Project["项目实践"]
        P1["Sentinel-2<br/>采样周期 5天"]
        P2["NDVI 时序<br/>离散信号 x[n]"]
        P3["插值 → 均匀采样<br/>fs = 1次/天"]
        P4["FFT 频谱<br/>幅度谱/功率谱"]
        P5["主周期提取<br/>Top 3 频率分量"]
    end
    
    subgraph Exam["892 信号与系统"]
        E1["采样定理<br/>fs ≥ 2fmax"]
        E2["离散时间信号<br/>序列 x[n]"]
        E3["DFT / FFT<br/>频谱分析"]
        E4["频域特征<br/>幅度/相位/功率"]
        E5["滤波器设计<br/>去噪/增强"]
    end
    
    P1 -.->|"对应"| E1
    P2 -.->|"对应"| E2
    P3 -.->|"对应"| E2
    P4 -.->|"对应"| E3
    P4 -.->|"对应"| E4
    P5 -.->|"对应"| E4
    P3 -.->|"滑动平均=低通滤波器"| E5
```

---

## 使用说明

1. **在 VS Code 中预览**：安装 Markdown Preview Mermaid Support 插件，按 `Ctrl+Shift+V` 预览
2. **在 GitHub 中预览**：直接 push，GitHub 会自动渲染 Mermaid 图表
3. **导出为图片**：使用 https://mermaid.live 复制粘贴代码，导出 PNG
