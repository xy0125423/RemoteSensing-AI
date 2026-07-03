"""
timeseries.py — NDVI 时间序列构建与分析模块

功能:
    1. 从逐景 NDVI 统计值构建时间序列
    2. 插值填充缺失日期（线性 / 样条）
    3. 滑动窗口平滑
    4. 趋势提取与分解
"""

import numpy as np
import pandas as pd
from scipy import interpolate, signal
import logging

logger = logging.getLogger(__name__)


def build_timeseries(
    dates: list[str],
    ndvi_values: list[float],
) -> pd.DataFrame:
    """构建 NDVI 时间序列 DataFrame。

    Args:
        dates: 日期字符串列表 ("YYYY-MM-DD")
        ndvi_values: 对应的 NDVI 均值列表

    Returns:
        DataFrame:
            index = datetime64
            columns = ["ndvi", "day_of_year"]
    """
    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "ndvi": ndvi_values,
    })
    df = df.sort_values("date").set_index("date")
    df["day_of_year"] = df.index.dayofyear
    return df


def interpolate_gaps(
    df: pd.DataFrame,
    method: str = "linear",
    freq: str = "5D",
) -> pd.DataFrame:
    """插值填充时间序列中的缺失日期。

    Args:
        df: 含 ndvi 列的 DataFrame（可能含 NaN）
        method: 插值方法 ("linear" | "spline" | "cubic")
        freq: 重采样频率 ("D" | "5D" | "W")

    Returns:
        插值后的 DataFrame（等间隔）
    """
    # 先重采样到固定频率
    df_resampled = df.resample(freq).mean()
    if method == "linear":
        df_resampled["ndvi"] = df_resampled["ndvi"].interpolate(method="linear")
    elif method in ("spline", "cubic"):
        df_resampled["ndvi"] = df_resampled["ndvi"].interpolate(
            method="spline", order=3
        )
    df_resampled["day_of_year"] = df_resampled.index.dayofyear
    return df_resampled


def smooth_savgol(
    df: pd.DataFrame,
    window: int = 7,
    polyorder: int = 2,
) -> pd.DataFrame:
    """Savitzky-Golay 平滑滤波。

    Args:
        df: 含 ndvi 列的 DataFrame
        window: 滑动窗口大小（奇数）
        polyorder: 多项式阶数

    Returns:
        DataFrame，新增 "ndvi_smooth" 列
    """
    if window % 2 == 0:
        window += 1
    df = df.copy()
    df["ndvi_smooth"] = signal.savgol_filter(
        df["ndvi"].fillna(method="ffill").fillna(method="bfill"),
        window_length=window,
        polyorder=polyorder,
    )
    return df


def decompose_trend(
    df: pd.DataFrame,
    period: int = 36,
) -> dict:
    """时间序列分解：趋势 + 季节 + 残差。

    Args:
        df: 含 ndvi 列的等间隔 DataFrame
        period: 季节周期（5天重采样 = 一年约 73 个点）

    Returns:
        {"trend": array, "seasonal": array, "residual": array}
    """
    # TODO: 使用 statsmodels seasonal_decompose 实现
    raise NotImplementedError("decompose_trend() 待实现")
