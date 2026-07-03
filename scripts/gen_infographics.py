"""
RemoteSensing-AI Infographic Generator — 9 high-quality 1920x1080 PNGs
Fonts: Noto Sans SC (CJK) + Segoe UI Emoji
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.font_manager import FontProperties
import numpy as np
import os

# ── Font Setup ─────────────────────────────────────────────────
# Register CJK + Emoji fonts
import matplotlib.font_manager as fm
for fp in fm.fontManager.ttflist:
    if 'NotoSansSC' in fp.fname and 'Regular' in fp.style:
        fm.fontManager.addfont(fp.fname)
        plt.rcParams['font.family'] = fp.name

# Try to use Noto Sans SC for CJK support
CJK_FONT = 'Noto Sans SC'
EMOJI_FONT = 'Segoe UI Emoji'
EN_FONT = 'DejaVu Sans'

# Verify CJK font works
try:
    fig_test, ax_test = plt.subplots(figsize=(1,1))
    ax_test.text(0,0, '测试', fontfamily=CJK_FONT)
    plt.close(fig_test)
    print(f"Using CJK font: {CJK_FONT}")
except:
    CJK_FONT = 'Microsoft YaHei'
    print(f"Fallback CJK font: {CJK_FONT}")

FONT = CJK_FONT  # primary font

# ── Color Palette ─────────────────────────────────────────────
BG      = '#FAFAFA'
CARD_BG = '#FFFFFF'
TEXT    = '#1D1D1F'
MUTED   = '#86868B'
ACCENT  = '#007AFF'
GREEN   = '#34C759'
ORANGE  = '#FF9500'
RED     = '#FF3B30'
PURPLE  = '#AF52DE'
TEAL    = '#5AC8FA'
PINK    = '#FF2D55'
YELLOW  = '#FFCC00'
GRAY_BG = '#F2F2F7'
DARK_BG = '#1C1C1E'

PHASE_COLORS = {
    'P0': GREEN, 'P1': ACCENT, 'P2': TEAL,
    'P3': ORANGE, 'P4': PURPLE, 'P5': PINK, 'P6': DARK_BG,
}

# ── Helpers ───────────────────────────────────────────────────
def new_fig(title_text="", subtitle_text=""):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)
    ax.set_facecolor(BG)
    ax.axis('off')
    fig.patch.set_facecolor(BG)
    # Dark title bar
    bar = FancyBboxPatch((0, 920), 1920, 160, boxstyle="round,pad=0",
                          facecolor=DARK_BG, edgecolor='none', zorder=0)
    ax.add_patch(bar)
    ax.text(60, 1012, title_text, fontsize=42, fontweight='bold',
            color='white', va='center', fontfamily=FONT)
    if subtitle_text:
        ax.text(60, 955, subtitle_text, fontsize=17, color='#AEAEB2',
                va='center', fontfamily=FONT)
    return fig, ax

def card(ax, x, y, w, h, color=CARD_BG, shadow=True, radius=16):
    if shadow:
        s = FancyBboxPatch((x+5, y-5), w, h, boxstyle=f"round,pad={radius/10}",
                            facecolor='#00000012', edgecolor='none', zorder=0)
        ax.add_patch(s)
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={radius/10}",
                        facecolor=color, edgecolor='#E5E5EA', linewidth=1.5, zorder=1)
    ax.add_patch(p)
    return p

def module_box(ax, x, y, w, h, emoji, title, desc, color=ACCENT):
    card(ax, x, y, w, h, color='white')
    bar = FancyBboxPatch((x, y), 6, h, boxstyle="round,pad=0",
                          facecolor=color, edgecolor='none', zorder=2)
    ax.add_patch(bar)
    ax.text(x+22, y+h-30, emoji, fontsize=26, va='top', fontfamily=EMOJI_FONT)
    ax.text(x+22, y+h-60, title, fontsize=14, fontweight='bold', color=TEXT,
            va='top', fontfamily=FONT)
    ax.text(x+22, y+h-82, desc, fontsize=11, color=MUTED, va='top', fontfamily=FONT)


# ═══════════════════════════════════════════════════════════════
# 1. PROJECT OVERVIEW
# ═══════════════════════════════════════════════════════════════
def gen_overview():
    fig, ax = new_fig("RemoteSensing-AI 项目总览",
                       "[输入地名] -> [GEE获取数据] -> [NDVI分析] -> [时序+FFT] -> [一键PDF报告]  |  CPU Only  |  2026.07-12")

    # Left: What
    card(ax, 40, 510, 590, 380)
    ax.text(72, 858, "项目做什么", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)
    steps = [
        ("1", "输入地名", "例如：山东省菏泽市郓城县", ACCENT),
        ("2", "GEE获取Sentinel-2影像", "云量过滤 < 10%", TEAL),
        ("3", "计算NDVI植被指数", "逐景计算并保存CSV", GREEN),
        ("4", "时间序列 + FFT频谱", "插值 -> 平滑 -> 周期提取", PURPLE),
        ("5", "生成PDF分析报告", "地图+折线图+频谱图+统计表", PINK),
    ]
    for i, (num, title, desc, color) in enumerate(steps):
        y_pos = 820 - i * 62
        circle = plt.Circle((85, y_pos+12), 17, color=color, zorder=3)
        ax.add_patch(circle)
        ax.text(85, y_pos+12, num, fontsize=13, fontweight='bold', color='white',
                ha='center', va='center', fontfamily=FONT)
        ax.text(120, y_pos+12, title, fontsize=16, fontweight='bold', color=TEXT,
                va='center', fontfamily=FONT)
        ax.text(120, y_pos-14, desc, fontsize=12, color=MUTED, va='center', fontfamily=FONT)

    # Right: Pipeline
    card(ax, 670, 510, 1220, 380)
    ax.text(700, 858, "技术路线", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)

    pipeline = [
        ("GEE获取", "Sentinel-2\nImageCollection", ACCENT),
        ("云量过滤", "CLOUDY < 10%\n28景影像", GREEN),
        ("NDVI计算", "(NIR-Red)\n/(NIR+Red)", TEAL),
        ("时间序列", "插值+平滑\n物候提取", ORANGE),
        ("FFT频谱", "scipy.rfft\n主周期提取", PURPLE),
        ("可视化", "地图+折线\n+频谱图", PINK),
        ("PDF报告", "fpdf2\n自动排版", DARK_BG),
    ]
    for i, (title, desc, color) in enumerate(pipeline):
        x_pos = 690 + i * 165
        card(ax, x_pos, 580, 150, 280, color='white', radius=14)
        header = FancyBboxPatch((x_pos, 820), 150, 46, boxstyle="round,pad=0",
                                 facecolor=color, edgecolor='none', zorder=2)
        ax.add_patch(header)
        ax.text(x_pos+75, 843, title, fontsize=12, fontweight='bold', color='white',
                ha='center', va='center', fontfamily=FONT)
        ax.text(x_pos+75, 750, desc, fontsize=11, color=TEXT, ha='center',
                va='center', fontfamily=FONT, linespacing=1.6)
        if i < len(pipeline) - 1:
            ax.annotate('', xy=(x_pos+145, 750), xytext=(x_pos+170, 750),
                       arrowprops=dict(arrowstyle='->', color=ORANGE, lw=3))

    # Bottom Left: Tech Stack
    card(ax, 40, 40, 720, 440)
    ax.text(72, 450, "技术栈", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)
    tech = [
        ("数据获取", "GEE Python API, Sentinel-2 L2A", GREEN),
        ("数据处理", "rasterio, numpy, scipy, pandas", ACCENT),
        ("可视化", "matplotlib", ORANGE),
        ("PDF生成", "fpdf2 / ReportLab", PURPLE),
        ("工程化", "Git, PyYAML, logging, pytest", DARK_BG),
    ]
    for i, (label, tools, color) in enumerate(tech):
        y_pos = 400 - i * 65
        card(ax, 70, y_pos-8, 660, 50, color=GRAY_BG, radius=10)
        tag = FancyBboxPatch((70, y_pos-8), 130, 50, boxstyle="round,pad=0",
                              facecolor=color, edgecolor='none', zorder=2)
        ax.add_patch(tag)
        ax.text(135, y_pos+17, label, fontsize=14, fontweight='bold', color='white',
                ha='center', va='center', fontfamily=FONT)
        ax.text(220, y_pos+17, tools, fontsize=13, color=TEXT, va='center', fontfamily=FONT)

    # Bottom Right: Principles
    card(ax, 790, 40, 1100, 440)
    ax.text(820, 450, "设计原则", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)
    principles = [
        ("能跑 > 完美", "每个 Phase 结束项目都必须可运行", GREEN),
        ("模块化 > 一体化", "每个 .py 文件独立可测试", ACCENT),
        ("文档 > 记忆", "所有决策、踩坑写入文档体系", ORANGE),
        ("简单 > 炫技", "CPU Only, 不依赖GPU, 不涉及深度学习", PURPLE),
        ("学习优先", "理解原理比调库更重要", PINK),
    ]
    for i, (title, desc, color) in enumerate(principles):
        y_pos = 400 - i * 70
        card(ax, 820, y_pos, 1040, 55, color=GRAY_BG, radius=12)
        dot = plt.Circle((850, y_pos+27), 12, color=color, zorder=3)
        ax.add_patch(dot)
        ax.text(880, y_pos+31, title, fontsize=16, fontweight='bold', color=TEXT,
                va='center', fontfamily=FONT)
        ax.text(880, y_pos+10, desc, fontsize=12, color=MUTED, va='center', fontfamily=FONT)

    fig.savefig('outputs/infographic_01_overview.png', dpi=100, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print("OK 01_overview")


# ═══════════════════════════════════════════════════════════════
# 2. PROJECT ROADMAP
# ═══════════════════════════════════════════════════════════════
def gen_roadmap():
    fig, ax = new_fig("项目路线图",
                       "7个Phase线性推进  |  总计约540小时  |  2026年7月 - 12月")

    phases = [
        ("P0", "环境搭建", "07/01-02", "6h", "完成", GREEN,
         ["Python环境", "GEE注册", "筛选28景"]),
        ("P1", "GeoTIFF驯服", "07/03-20", "54h", "当前", ACCENT,
         ["GEE导出", "rasterio读取", "真彩色显示"]),
        ("P2", "NDVI引擎", "07/21-08/15", "78h", "待开始", TEAL,
         ["手写NDVI", "批量计算", "CSV输出"]),
        ("P3", "时间序列", "08/16-09/15", "93h", "待开始", ORANGE,
         ["插值", "平滑", "物候提取"]),
        ("P4", "FFT频谱", "09/16-10/20", "105h", "待开始", PURPLE,
         ["scipy.rfft", "频谱图", "主周期"]),
        ("P5", "可视化PDF", "10/21-11/20", "93h", "待开始", PINK,
         ["图表美化", "fpdf2", "中文PDF"]),
        ("P6", "系统集成", "11/21-12/31", "123h", "待开始", DARK_BG,
         ["一键运行", "3份报告", "完善README"]),
    ]

    for i, (pid, name, dates, hours, status, color, outputs) in enumerate(phases):
        x_pos = 40 + i * 268
        y_top = 870
        w = 252

        card(ax, x_pos, y_top-340, w, 380, color='white', radius=16)

        # Phase header
        hdr = FancyBboxPatch((x_pos, y_top-52), w, 52, boxstyle="round,pad=0",
                              facecolor=color, edgecolor='none', zorder=2)
        ax.add_patch(hdr)
        ax.text(x_pos+w/2, y_top-26, f"{pid}  {name}", fontsize=15, fontweight='bold',
                color='white', ha='center', va='center', fontfamily=FONT)

        # Date & Hours
        ax.text(x_pos+20, y_top-90, dates, fontsize=13, color=TEXT, fontfamily=FONT)
        ax.text(x_pos+20, y_top-118, hours, fontsize=13, color=TEXT, fontfamily=FONT)

        # Status badge
        status_color = GREEN if status == "完成" else (color if status == "当前" else '#E5E5EA')
        status_text_color = 'white' if status in ("完成", "当前") else MUTED
        badge = FancyBboxPatch((x_pos+20, y_top-155), 72, 26, boxstyle="round,pad=4",
                                facecolor=status_color, edgecolor='none', zorder=2)
        ax.add_patch(badge)
        ax.text(x_pos+56, y_top-142, status, fontsize=11, fontweight='bold',
                color=status_text_color, ha='center', va='center', fontfamily=FONT)

        # Outputs
        ax.text(x_pos+20, y_top-185, "输出:", fontsize=12, fontweight='bold', color=TEXT,
                fontfamily=FONT)
        for j, out in enumerate(outputs):
            ax.text(x_pos+30, y_top-210-j*22, out, fontsize=11, color=MUTED, fontfamily=FONT)

        # Arrow between phases
        if i < len(phases) - 1:
            ax.annotate('', xy=(x_pos+w-10, y_top-210), xytext=(x_pos+w+20, y_top-210),
                       arrowprops=dict(arrowstyle='->', color='#C7C7CC', lw=2.5))

    # Bottom: Timeline
    card(ax, 40, 360, 1840, 70, color=DARK_BG, radius=16)
    months = ['7月', '8月', '9月', '10月', '11月', '12月']
    mcolors = [ACCENT, TEAL, ORANGE, PURPLE, PINK, DARK_BG]
    for i, (m, c) in enumerate(zip(months, mcolors)):
        x_pos = 80 + i * 300
        circle = plt.Circle((x_pos+30, 395), 16, color=c, zorder=3)
        ax.add_patch(circle)
        ax.text(x_pos+55, 395, m, fontsize=22, fontweight='bold', color='white',
                va='center', fontfamily=FONT)

    # Milestones
    card(ax, 40, 40, 1840, 290, color='white', radius=16)
    ax.text(72, 300, "关键里程碑", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)
    milestones = [
        ("07.20", "5景GeoTIFF本地", "Phase1完成", GREEN),
        ("08.24", "NDVI CSV输出", "Phase2完成", ACCENT),
        ("09.21", "插值序列就绪", "Phase3完成", ORANGE),
        ("10.20", "频谱图+主周期", "Phase4完成", PURPLE),
        ("11.20", "第一份PDF报告", "Phase5完成", PINK),
        ("12.31", "一键运行+3报告", "Phase6完成", DARK_BG),
    ]
    for i, (date, desc, phase, color) in enumerate(milestones):
        x_pos = 70 + i * 305
        card(ax, x_pos, 70, 280, 190, color=GRAY_BG, radius=14)
        bar = FancyBboxPatch((x_pos, 240), 280, 6, boxstyle="round,pad=0",
                              facecolor=color, edgecolor='none', zorder=3)
        ax.add_patch(bar)
        ax.text(x_pos+140, 200, date, fontsize=32, fontweight='bold', color=color,
                ha='center', fontfamily=FONT)
        ax.text(x_pos+140, 150, desc, fontsize=15, color=TEXT, ha='center', fontfamily=FONT)
        ax.text(x_pos+140, 115, phase, fontsize=13, color=MUTED, ha='center', fontfamily=FONT)

    fig.savefig('outputs/infographic_02_roadmap.png', dpi=100, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print("OK 02_roadmap")


# ═══════════════════════════════════════════════════════════════
# 3. TASK ROADMAP
# ═══════════════════════════════════════════════════════════════
def gen_tasks():
    fig, ax = new_fig("任务路线图",
                       "40个独立Task  |  每个1-3小时  |  每天完成一个即可  |  按Phase分组")

    phases_tasks = [
        ("P1 GeoTIFF", ACCENT, 40, 7, ["T01\n导出", "T02\n下载", "T03\n元数据", "T04\n波段", "T05\n显示", "T06\n批量", "T07\n汇总"]),
        ("P2 NDVI", TEAL, 310, 7, ["T08\n手算", "T09\n函数", "T10\n伪彩", "T11\n对比", "T12\nCSV", "T13\n时序", "T14\n决策"]),
        ("P3 时序", ORANGE, 580, 6, ["T15\n折线", "T16\n异常", "T17\n插值", "T18\n平滑", "T19\n物候", "T20\n对比"]),
        ("P4 FFT", PURPLE, 850, 6, ["T21\n验证", "T22\n频谱", "T23\n周期", "T24\n笔记", "T25\n对比", "T26\n注释"]),
        ("P5 PDF", PINK, 1120, 7, ["T27\n设计", "T28\n封面", "T29\n地图", "T30\n时序", "T31\n频谱", "T32\nPDF", "T33\n审查"]),
        ("P6 集成", DARK_BG, 1390, 7, ["T34\n坐标", "T35\n配置", "T36\n流水线", "T37\n日志", "T38\n测试", "T39\n文档", "T40\n报告"]),
    ]

    for phase_name, color, x_start, count, tasks in phases_tasks:
        hw = count * 84 + 10
        hdr = FancyBboxPatch((x_start, 875), hw, 42, boxstyle="round,pad=8",
                              facecolor=color, edgecolor='none', zorder=2)
        ax.add_patch(hdr)
        ax.text(x_start + hw/2, 896, phase_name, fontsize=14, fontweight='bold',
                color='white', ha='center', va='center', fontfamily=FONT)

        for j, task in enumerate(tasks):
            tx = x_start + j * 84
            ty = 815
            tc = FancyBboxPatch((tx, ty), 76, 38, boxstyle="round,pad=5",
                                 facecolor='white', edgecolor=color, linewidth=2, zorder=2)
            ax.add_patch(tc)
            ax.text(tx+38, ty+19, task, fontsize=8, fontweight='bold', color=color,
                    ha='center', va='center', fontfamily=FONT, linespacing=1.2)

    # Stats bar
    card(ax, 40, 680, 1840, 110, color=DARK_BG, radius=16)
    stats = [("40", "总任务"), ("28", "核心必做"), ("10", "重要推荐"), ("3", "可选进阶"),
             ("96h", "纯开发"), ("540h", "含学习缓冲")]
    for i, (num, label) in enumerate(stats):
        x_pos = 100 + i * 300
        ax.text(x_pos+100, 750, num, fontsize=44, fontweight='bold', color='white',
                ha='center', fontfamily=FONT)
        ax.text(x_pos+100, 705, label, fontsize=15, color='#AEAEB2', ha='center', fontfamily=FONT)

    # Bottom: Daily flow
    card(ax, 40, 40, 1840, 610, color='white', radius=16)
    ax.text(72, 620, "每日执行流程", fontsize=22, fontweight='bold', color=TEXT, fontfamily=FONT)

    flow = [
        ("19:00", "打开TASK\nROADMAP", "找下一个[ ]Task", ACCENT),
        ("19:05", "阅读任务", "描述+依赖+标志", TEAL),
        ("19:10", "写代码", "1-3小时专注", ORANGE),
        ("22:00", "完成标志", "打[x]标记", GREEN),
        ("22:10", "记录笔记", "写入TODAY.md", PURPLE),
    ]
    for i, (time_label, title, desc, color) in enumerate(flow):
        x_pos = 70 + i * 360
        outer = plt.Circle((x_pos+110, 440), 65, color=color, zorder=3, alpha=0.12)
        ax.add_patch(outer)
        inner = plt.Circle((x_pos+110, 440), 48, color=color, zorder=4)
        ax.add_patch(inner)
        ax.text(x_pos+110, 440, time_label, fontsize=18, fontweight='bold', color='white',
                ha='center', va='center', fontfamily=FONT)
        ax.text(x_pos+110, 350, title, fontsize=15, fontweight='bold', color=TEXT,
                ha='center', fontfamily=FONT, linespacing=1.3)
        ax.text(x_pos+110, 300, desc, fontsize=12, color=MUTED, ha='center', fontfamily=FONT)

        if i < len(flow) - 1:
            ax.annotate('', xy=(x_pos+260, 440), xytext=(x_pos+290, 440),
                       arrowprops=dict(arrowstyle='->', color='#C7C7CC', lw=3.5))

    # Task type legend
    card(ax, 70, 100, 560, 120, color=GRAY_BG, radius=12)
    legends = [("核心必做 28个", RED), ("重要推荐 10个", ORANGE), ("可选进阶 3个", GREEN)]
    for i, (label, color) in enumerate(legends):
        dot = plt.Circle((110+i*180, 160), 10, color=color, zorder=3)
        ax.add_patch(dot)
        ax.text(130+i*180, 160, label, fontsize=14, fontweight='bold', color=TEXT,
                va='center', fontfamily=FONT)

    fig.savefig('outputs/infographic_03_tasks.png', dpi=100, bbox_inches='tight',
                facecolor=BG, edgecolor='none')
    plt.close(fig)
    print("OK 03_tasks")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    gen_overview()
    gen_roadmap()
    gen_tasks()
    print("\n=== First 3 infographics done ===")
