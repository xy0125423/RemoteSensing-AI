"""
fft_analyzer.py — 傅里叶频谱分析模块

功能:
    1. 对 NDVI 时间序列做 FFT 变换
    2. 提取主频成分（年周期 / 半年周期）
    3. 谐波重建
    4. 周期显著性检验
"""

import numpy as np
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy import signal
import logging

logger = logging.getLogger(__name__)


def apply_window(
    signal_data: np.ndarray,
    window_type: str = "hann",
) -> np.ndarray:
    """对信号加窗以减少频谱泄漏。

    Args:
        signal_data: 一维信号数组
        window_type: 窗函数类型 ("hann" | "hamming" | "blackman" | "none")

    Returns:
        加窗后的信号数组
    """
    n = len(signal_data)
    if window_type == "hann":
        window = signal.windows.hann(n)
    elif window_type == "hamming":
        window = signal.windows.hamming(n)
    elif window_type == "blackman":
        window = signal.windows.blackman(n)
    elif window_type == "none":
        window = np.ones(n)
    else:
        raise ValueError(f"未知窗函数类型: {window_type}")
    return signal_data * window


def detrend(
    signal_data: np.ndarray,
    method: str = "linear",
) -> np.ndarray:
    """去除信号趋势。

    Args:
        signal_data: 一维信号数组
        method: "linear" | "mean" | "none"

    Returns:
        去趋势后的信号数组
    """
    if method == "linear":
        return signal.detrend(signal_data, type="linear")
    elif method == "mean":
        return signal_data - np.mean(signal_data)
    elif method == "none":
        return signal_data
    else:
        raise ValueError(f"未知去趋势方法: {method}")


def compute_fft(
    signal_data: np.ndarray,
    dt: float = 5.0,
) -> dict:
    """计算一维信号的 FFT 频谱。

    Args:
        signal_data: 输入信号（等间隔采样）
        dt: 采样间隔（天）

    Returns:
        {
            "freqs": array,          # 频率 (1/天)
            "periods": array,        # 周期 (天)
            "amplitude": array,      # 振幅
            "phase": array,          # 相位
            "power": array,          # 功率谱密度
        }
    """
    n = len(signal_data)
    yf = rfft(signal_data)
    freqs = rfftfreq(n, d=dt)
    amplitude = np.abs(yf) / n * 2  # 归一化
    phase = np.angle(yf)
    power = amplitude ** 2

    # 避免除零
    periods = np.where(freqs > 0, 1.0 / freqs, np.inf)

    return {
        "freqs": freqs,
        "periods": periods,
        "amplitude": amplitude,
        "phase": phase,
        "power": power,
    }


def find_dominant_periods(
    fft_result: dict,
    top_n: int = 5,
    min_period: float = 10.0,
    max_period: float = 730.0,
) -> list[dict]:
    """提取频谱中振幅最强的 N 个周期成分。

    Args:
        fft_result: compute_fft() 返回的字典
        top_n: 返回前 N 个周期
        min_period: 最小考虑周期（天）
        max_period: 最大考虑周期（天）

    Returns:
        [{"period": float, "amplitude": float, "phase": float}, ...]
        按振幅降序排列
    """
    periods = fft_result["periods"]
    amplitude = fft_result["amplitude"]
    phase = fft_result["phase"]

    # 筛选周期范围
    mask = (
        (periods >= min_period)
        & (periods <= max_period)
        & np.isfinite(periods)
    )
    valid_idx = np.where(mask)[0]

    if len(valid_idx) == 0:
        logger.warning("指定周期范围内无有效频率成分")
        return []

    # 按振幅排序
    sorted_idx = valid_idx[np.argsort(amplitude[valid_idx])[::-1]]
    top_idx = sorted_idx[:top_n]

    return [
        {
            "period": float(periods[i]),
            "amplitude": float(amplitude[i]),
            "phase": float(phase[i]),
        }
        for i in top_idx
    ]


def reconstruct_harmonics(
    fft_result: dict,
    top_n: int = 3,
) -> np.ndarray:
    """用前 N 个主频率谐波重建信号。

    Args:
        fft_result: compute_fft() 返回的字典
        top_n: 使用的谐波数量

    Returns:
        重建的一维信号数组
    """
    # TODO: 实现谐波重建
    raise NotImplementedError("reconstruct_harmonics() 待实现")
