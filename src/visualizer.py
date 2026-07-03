"""
visualizer.py — 可视化模块

功能:
    1. NDVI 空间分布地图（叠加行政边界）
    2. NDVI 时间序列折线图
    3. FFT 频谱图
    4. 多子图组合排版
    5. 中文字体支持
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# ---- 全局绘图样式 ----
plt.rcParams["figure.dpi"] = 150
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["savefig.bbox"] = "tight"


def set_font(font_path: str = None) -> None:
    """设置 Matplotlib 中文字体。

    Args:
        font_path: .ttf 字体文件路径，默认查找 data/fonts/ 目录
    """
    if font_path is None:
        font_path = str(
            Path(__file__).parent.parent / "data" / "fonts" / "SimHei.ttf"
        )

    if Path(font_path).exists():
        from matplotlib.font_manager import FontProperties
        font_prop = FontProperties(fname=font_path)
        plt.rcParams["font.family"] = font_prop.get_name()
        logger.info("字体加载成功: %s", font_path)
    else:
        logger.warning(
            "中文字体文件未找到 (%s)，图表中文可能显示为方框。"
            "请将 .ttf 字体文件放入 data/fonts/ 目录。",
            font_path,
        )


def plot_ndvi_map(
    ndvi_array: np.ndarray,
    transform,
    boundary,
    save_path: str,
    title: str = "NDVI 空间分布",
    cmap: str = "RdYlGn",
    vmin: float = -1.0,
    vmax: float = 1.0,
) -> str:
    """绘制 NDVI 空间分布地图。

    Args:
        ndvi_array: NDVI 2D 数组
        transform: 仿射变换
        boundary: 行政边界 Shapely 对象
        save_path: 保存路径 (.png)
        title: 图表标题
        cmap: 颜色映射
        vmin, vmax: 色彩范围

    Returns:
        保存的文件路径
    """
    # TODO: 实现地图绘制
    raise NotImplementedError("plot_ndvi_map() 待实现")


def plot_timeseries(
    df: pd.DataFrame,
    save_path: str,
    title: str = "NDVI 时间序列",
    ylabel: str = "NDVI",
) -> str:
    """绘制 NDVI 时间序列折线图。

    Args:
        df: 含 ndvi 列（和可选的 ndvi_smooth 列）的 DataFrame
        save_path: 保存路径
        title: 图表标题
        ylabel: Y 轴标签

    Returns:
        保存的文件路径
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df.index, df["ndvi"], "o-", markersize=3, alpha=0.4,
            color="gray", label="原始值")
    if "ndvi_smooth" in df.columns:
        ax.plot(df.index, df["ndvi_smooth"], "-", linewidth=2,
                color="#2c7bb6", label="平滑值")

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("日期")
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    fig.savefig(save_path)
    plt.close(fig)
    logger.info("时间序列图已保存: %s", save_path)
    return save_path


def plot_fft_spectrum(
    fft_result: dict,
    save_path: str,
    title: str = "FFT 频谱分析",
    top_periods: list[dict] = None,
) -> str:
    """绘制 FFT 频谱图（振幅 + 功率谱）。

    Args:
        fft_result: compute_fft() 返回的字典
        save_path: 保存路径
        title: 图表标题
        top_periods: find_dominant_periods() 的结果，用于标注

    Returns:
        保存的文件路径
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    periods = fft_result["periods"]
    amplitude = fft_result["amplitude"]
    power = fft_result["power"]

    # 只显示正周期
    mask = np.isfinite(periods) & (periods > 0) & (periods < 730)
    p = periods[mask]
    a = amplitude[mask]
    pw = power[mask]

    # 振幅谱
    ax1.stem(p, a, basefmt=" ", linefmt="C0-", markerfmt="C0o")
    ax1.set_xlabel("周期 (天)")
    ax1.set_ylabel("振幅")
    ax1.set_title(title)
    ax1.grid(True, alpha=0.3)

    # 标记主周期
    if top_periods:
        for tp in top_periods:
            ax1.axvline(tp["period"], color="red", linestyle="--", alpha=0.5)
            ax1.annotate(
                f"{tp['period']:.0f}d",
                xy=(tp["period"], tp["amplitude"]),
                xytext=(5, 5), textcoords="offset points",
                color="red", fontsize=9,
            )

    # 功率谱
    ax2.plot(p, pw, "C1-", linewidth=1)
    ax2.set_xlabel("周期 (天)")
    ax2.set_ylabel("功率")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
    logger.info("FFT 频谱图已保存: %s", save_path)
    return save_path
