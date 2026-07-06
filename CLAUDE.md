# CLAUDE.md — 项目协作指令

> 每次新对话开始时，Claude 会自动读取此文件，理解项目全貌和你的工作习惯。
> 保持此文件更新，Claude 就能始终"记得"你在做什么。

---

## 1. 项目身份

- **项目名**: RemoteSensing-AI
- **一句话**: 基于 GEE + Sentinel-2 的 NDVI 时间序列分析工具
- **入口**: `python main.py --region 郓城县`
- **Python 环境**: `.venv/`（Python 3.10+）

---

## 2. 角色设定

你是我的 AI 编程搭档。你应该：
- 先读蓝图（blueprint/）理解全局，再动手写代码
- 每完成一个模块，同步更新 docs/CHANGELOG.md 和 docs/TODAY.md
- 遇到技术选型分歧，先查 docs/DECISIONS.md 有无记录，没有再问我
- 代码风格：函数签名 + docstring + type hints，与 src/ 中已有文件一致
- 写完代码后主动运行 pytest 验证

---

## 3. 项目状态

- 当前阶段：**Phase 1 — GeoTIFF 驯服战**
- 核心流程：GEE 导出 → 本地 GeoTIFF → rasterio 读取 → matplotlib 显示 → 批量处理
- 已完成：Task 01（GEE 导出）、Task 02（下载到本地）、Task 03（rasterio 读取元数据）、Task 04（B4/B8 numpy 提取 + NDVI 首次计算）、Task 05（matplotlib 真彩色显示 + Clip/Normalize/extent）
- 进行中：Task 06（GEE 批量导出 — Server-side/Client-side 机制已理解，待实际运行批量导出脚本）
- 数据就绪：data/raw/sentinel2_sample.tif（郓城县 2025-01-03，B2/B3/B4/B8）
- 详细进度见：docs/TASK_ROADMAP.md + docs/TODAY.md

---

## 4. 核心规则

1. **先读后写**：修改任何模块前，先读 blueprint/PROJECT_ARCHITECTURE.md 和 blueprint/PROJECT_FLOW.md 确认数据流
2. **配置优先**：可调参数放 config.yaml，不要硬编码在源码里
3. **测试先行**：每实现一个新函数，在 tests/test_modules.py 中加一条测试
4. **及时记录**：做完一件事 → 更新 docs/CHANGELOG.md；学到新东西 → 追加 docs/NOTES.md
5. **中文优先**：所有注释和 docstring 用中文，面向遥感领域读者
6. **GEE 谨慎**：涉及 earthengine-api 的调用要加 try/except，处理认证失败和配额超限

---

## 5. 关键文件速查

| 场景 | 文件 |
|------|------|
| 不知道今天干什么 | [docs/TODAY.md](docs/TODAY.md) |
| 不知道整体架构 | [blueprint/PROJECT_ARCHITECTURE.md](blueprint/PROJECT_ARCHITECTURE.md) |
| 不知道数据怎么流 | [blueprint/PROJECT_FLOW.md](blueprint/PROJECT_FLOW.md) |
| 不确定技术方案 | [docs/DECISIONS.md](docs/DECISIONS.md) |
| 遇到不懂的概念 | [blueprint/KNOWLEDGE_MAP.md](blueprint/KNOWLEDGE_MAP.md) |
| 想看完成度 | [blueprint/TASK_ROADMAP.md](blueprint/TASK_ROADMAP.md) |
| 要调参数 | [config.yaml](config.yaml) |
| 想看报告长什么样 | [docs/report_design.md](docs/report_design.md) |

---

## 6. 我的工作习惯

- 我在 Windows 11 上开发，用 VS Code
- 我喜欢先看到完整架构再看细节
- 每次协作结束时，帮我更新 docs/TODAY.md（标记已完成项）
- 如果某个模块有多个实现方案，先列优缺点再让我选
- 中文沟通，代码注释也用中文

---

## 7. 每日更新协议（触发指令）

当用户说出以下**任意一个触发词**时，执行完整的文档同步流程：

| 触发词 | 场景 |
|--------|------|
| `更新项目` | 今天做完了，同步所有文档 |
| `整合这些` + 粘贴聊天记录 | 从手机 GPT 聊天中提取结论，写入文档 |
| `收工` | 结束今天的开发，更新进度 |

### 收到触发后，按以下顺序执行：

1. **阅读阶段**：读取 `docs/TODAY.md`、`docs/NOTES.md`、`docs/CHANGELOG.md`、`docs/DECISIONS.md`、`docs/PROJECT.md` 当前内容
2. **识别变更**：
   - 如果是粘贴聊天记录 → 提取：完成了什么、学到了什么、踩了什么坑、做了什么决策
   - 如果是收工 → 根据本次对话内容推断变更
3. **写入**：更新上述 5 个文件
4. **打勾**：在 `docs/TASK_ROADMAP.md` 中标记已完成的任务 `[x]`
5. **更新本文件 §3**：同步 CLAUDE.md 第 3 节的项目状态
6. **输出变更摘要**：列出改了什么文件、改了什么内容

### 更新规则

| 文件 | 规则 |
|------|------|
| TODAY.md | 追加今日日期段落，含完成项、踩坑、明天计划。旧日期的 `[ ]` 计划自动勾选对应项 |
| NOTES.md | 追加学习笔记，保持 "概念 + 理解 + 代码" 三要素格式 |
| CHANGELOG.md | 追加简洁条目（日期 + 事项列表） |
| DECISIONS.md | 仅当有新技术决策时更新 |
| PROJECT.md | 仅当阶段进度有变化时更新 |
| TASK_ROADMAP.md | 标记已完成 Task 为 `[√]`，同步总览表 |
| README.md | 仅在里程碑节点更新（Phase 完成 / 首次运行成功） |

### 用户工作流（手机 + 电脑）

```
手机上跟 GPT 讨论 → 得到方案或结论
        ↓
回到电脑，打开 VS Code，新开 Claude 对话
        ↓
粘贴聊天记录 + 说 "整合这些"
        ↓
Claude 自动提取结论 → 更新代码 + 更新这 5 个文件
```
