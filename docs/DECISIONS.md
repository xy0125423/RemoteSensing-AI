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


## 2026-07-04：GeoTIFF 必须先理解 Metadata，不得直接跳到 NDVI

- 问题：容易急于计算 NDVI，跳过了对数据结构的理解
- 决定：严格遵守以下学习顺序，不得跳步：
  1. 理解 Metadata（width、height、count、crs、resolution）
  2. 理解 Band Mapping（dataset.read() 的索引含义）
  3. 读取波段数据为 numpy 数组
  4. 验证波段间像素一一对应
  5. 最后才做 NDVI 计算
- 原因：
  - 不理解数据结构直接计算 → 结果对也不知道为什么对，错也不知道哪里错
  - Band Mapping 是后续所有波段运算的基础
  - 复试时导师可能问"你数据怎么读的"，需要能讲清楚每一步
- 原则：数据结构理解 > 公式计算，这是工程基本功

---

## 2026-07-04（续）：遥感计算统一使用 float32

- 问题：Sentinel-2 L2A GeoTIFF 存储为 uint16，直接做除法会丢失小数
- 决定：所有遥感指数计算前，统一将波段数据转为 float32
- 原因：
  - uint16 整数除法：5/2=2，NDVI 需要 0.667 → 结果是 0（完全错误）
  - float32 浮点除法：5.0/2.0=2.5，保留小数
  - float64 精度过高（15 位），浪费内存且无必要（NDVI 只需 2~3 位有效数字）
- 原则：遥感计算 = float32，float64 仅在精度关键的场景使用（如矩阵求逆）

---

## 2026-07-04（续）：保持 GeoTIFF 波段顺序与 GEE 导出顺序一致

- 问题：GeoTIFF 内部的波段编号与 Sentinel-2 原始波段编号不同，容易混淆
- 决定：在代码注释和文档中始终标注两者的映射关系，不尝试修改 GeoTIFF 内部波段顺序
- 原因：
  - 修改波段顺序可能引入新的 Bug
  - 保持导出原样，减少变量
  - 用文档记录映射关系，清晰可追溯
- 当前映射：read(1)=B2, read(2)=B3, read(3)=B4, read(4)=B8
- 原则：数据入库不改动，映射关系写入文档

---

## 2026-07-04（续）：先验证再计算（Verify-then-Compute）

- 问题：急于计算 NDVI，跳过数据验证步骤
- 决定：任何波段运算前，必须先验证三项：
  1. `shape` — 各波段形状一致（同一张影像）
  2. `dtype` — 数据类型已转为 float32
  3. 统计信息（min/max/mean/std）— 数值在合理范围（0~10000 for uint16, 0~1 for reflectance）
- 原因：
  - shape 不一致 → 运算会报错或产生错误结果
  - dtype 错误 → uint16 除法丢失小数，NDVI 全为 0 或 1
  - 统计信息异常 → 数据损坏、云覆盖、导出区域全是水体
- 原则：验证 → 计算 → 再验证（检查结果 NDVI 在 -1~1 范围内）

---

## 2026-07-05：遥感影像显示采用 Clip-first-then-Normalize 标准流程

- 问题：直接 `plt.imshow(rgb)` 显示遥感影像 → 一片白
- 决定：所有遥感影像显示必须遵循：读取 → Stack → Clip(2%, 98%) → Normalize(0, 1) → imshow
- 原因：
  - Sentinel-2 L2A DN 值范围远超 0~1（实际约 87~3580）
  - Matplotlib imshow 对 float 数据要求 0~1，超范围自动裁切
  - 先 Clip 去掉异常值，再 Normalize 映射到 0~1，才能保证正常区域有足够对比度
  - 如果先 Normalize 再 Clip（或只做其中一步），极端值占据动态范围，正常区域对比度极低
- 原则：Clip 负责去异常，Normalize 负责映射区间。两步各司其职，缺一不可，且 Clip → Normalize 顺序不可颠倒
- 对比：教材"2%~98% 线性拉伸" = 工程中的 Clip(2%, 98%) + Normalize(0, 1)，理论与工程实践一致

---

## 2026-07-05（续）：遥感算法 = NumPy 数组运算

- 认知：今天建立了贯穿整个项目的核心理解
- 决定：后续所有遥感算法（NDVI、NDWI、EVI、FFT）都应从"NumPy 数组运算"的视角去理解
- 原因：
  - NDVI = 逐元素四则运算：`(b8 - b4) / (b8 + b4)`
  - RGB 合成 = 数组堆叠：`np.stack([b4, b3, b2], axis=-1)`
  - Clip = 数组裁剪：`np.clip(rgb, low, high)`
  - Normalize = 区间映射：`(rgb - low) / (high - low)`
  - 所有"遥感算法"本质上是对数组的合理数学处理
- 原则：不把遥感算法神秘化，理解到 NumPy 层面即可自信实现

---

## 2026-07-07：GEE 批量操作优先使用 evaluate()，避免 getInfo()

- 问题：GEE 中需要将 ee.Number 转为 JavaScript Number 才能写 for 循环
- 决定：工程代码统一使用 `evaluate(callback)` 异步模式，避免 `getInfo()` 同步阻塞
- 原因：
  - `getInfo()` 同步等待服务器返回，浏览器可能卡顿，不适合批量处理
  - `evaluate()` 异步回调，服务器计算完成后才执行 callback，不阻塞 UI
  - 大型工程的批量导出需要稳定、不超时的通信方式
- 原则：evaluate() 优先，getInfo() 仅用于简单调试
- 例外：单次快速调试（如确认一个值），getInfo() 代码更短，可临时使用

---

## 2026-07-07（续）：GEE 批量导出采用 toList + for 循环，而非 .map()

- 问题：ImageCollection 需要拆开逐张 Export，两种方案可选
- 方案 A：`.map(function(img){return Export.image.toDrive(...)})` — 函数式
- 方案 B：`toList(n) → for → get(i) → ee.Image → Export` — 命令式
- 决定：当前阶段采用方案 B（toList + for）
- 原因：
  - 方案 B 每一步都显式可控，适合学习阶段理解每一步
  - for 循环中可以根据 i 灵活设置导出参数（文件名、区域等）
  - 方案 A 中 .map() 不保证执行顺序，且 Export 在 map 中行为复杂
- 原则：学习阶段选可理解性 > 简洁性；后续可重构为 .map()

---

## 2026-07-07（续）：工程化文件命名统一使用 yyyyMMdd 日期格式

- 问题：批量导出 28 景影像，文件名需要包含日期以便后续 Python 排序处理
- 决定：文件名格式统一为 `S2_yyyyMMdd`（如 `S2_20250315`）
- 原因：
  - 字典序 = 时间序 → Python `sorted(files)` 即按时间排列
  - 避免日期格式歧义（MM/dd vs dd/MM）
  - 为 Task 12 的 NDVI 时间序列分析（按日期排序）打基础
- 原则：文件名即元数据，格式设计要考虑到后续代码的便利性