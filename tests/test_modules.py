"""
test_modules.py — 核心模块单元测试

运行方式:
    pytest tests/test_modules.py -v
    python -m pytest tests/test_modules.py -v

测试覆盖:
    - config: 配置加载逻辑
    - geocode: 地名解析
    - ndvi_calc: NDVI 统计计算
    - timeseries: 时间序列操作
    - fft_analyzer: FFT 频谱分析
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# 将 src 加入搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


# ============================================================
#  config.py 测试
# ============================================================

class TestConfig:
    """配置加载测试。"""

    def test_default_config(self):
        """默认配置应包含所有必要字段。"""
        from config import get_default_config
        cfg = get_default_config()
        assert "time" in cfg
        assert "geo" in cfg
        assert "ndvi" in cfg
        assert "fft" in cfg
        assert "paths" in cfg

    def test_resolve_paths_creates_dirs(self, tmp_path):
        """resolve_paths 应自动创建不存在的目录。"""
        from config import resolve_paths
        cfg = {
            "paths": {
                "test_dir": str(tmp_path / "new_folder"),
            }
        }
        result = resolve_paths(cfg)
        assert Path(result["paths"]["test_dir"]).exists()


# ============================================================
#  ndvi_calc.py 测试
# ============================================================

class TestNDVICalc:
    """NDVI 计算测试。"""

    def test_compute_stats_basic(self):
        """基本统计值计算。"""
        from ndvi_calc import compute_stats
        data = np.array([
            [0.5, 0.6, np.nan],
            [0.7, -0.1, 0.3],  # -0.1 会被 snow mask 过滤
        ])
        stats = compute_stats(data, mask_snow=True)

        assert stats["valid_pixels"] == 4  # 排除 NaN 和负值
        assert 0.5 < stats["mean"] < 0.6
        assert stats["coverage"] == 4 / 6

    def test_compute_stats_all_nan(self):
        """全 NaN 数组应返回 NaN 而不报错。"""
        from ndvi_calc import compute_stats
        data = np.full((10, 10), np.nan)
        stats = compute_stats(data)
        assert np.isnan(stats["mean"])
        assert stats["valid_pixels"] == 0


# ============================================================
#  timeseries.py 测试
# ============================================================

class TestTimeSeries:
    """时间序列测试。"""

    def test_build_timeseries(self):
        """基本时间序列构建。"""
        from timeseries import build_timeseries
        dates = ["2023-01-01", "2023-01-06", "2023-01-11"]
        values = [0.5, 0.6, 0.55]
        df = build_timeseries(dates, values)
        assert len(df) == 3
        assert "ndvi" in df.columns
        assert "day_of_year" in df.columns

    def test_interpolate_gaps(self):
        """插值应填充缺失值。"""
        from timeseries import build_timeseries, interpolate_gaps
        dates = ["2023-01-01", "2023-01-11", "2023-01-21"]
        values = [0.5, 0.6, 0.55]
        df = build_timeseries(dates, values)
        df_interp = interpolate_gaps(df, method="linear", freq="5D")
        # 重采样到 5D 频率后应有更多记录
        assert len(df_interp) >= 3


# ============================================================
#  fft_analyzer.py 测试
# ============================================================

class TestFFTAnalyzer:
    """FFT 分析测试。"""

    def test_compute_fft_sine(self):
        """对纯正弦波做 FFT 应检出正确周期。"""
        from fft_analyzer import compute_fft, find_dominant_periods

        # 生成周期为 73（≈1年，5天采样）的正弦波
        dt = 5  # 天
        t = np.arange(0, 365, dt)
        period = 73  # 5*73 = 365 ≈ 1 年
        signal_data = np.sin(2 * np.pi * t / period)

        result = compute_fft(signal_data, dt=dt)
        dominant = find_dominant_periods(result, top_n=3)

        # 最强周期应接近 73
        assert len(dominant) > 0
        assert abs(dominant[0]["period"] - period) < 20

    def test_apply_window(self):
        """加窗不改变信号长度。"""
        from fft_analyzer import apply_window
        data = np.random.randn(100)
        windowed = apply_window(data, "hann")
        assert len(windowed) == len(data)
        # 加窗后两端衰减
        assert abs(windowed[0]) < abs(data[0])

    def test_detrend_linear(self):
        """线性去趋势后信号均值应接近 0。"""
        from fft_analyzer import detrend
        # 创建带线性趋势的信号
        t = np.linspace(0, 10, 100)
        data = 2 * t + np.sin(t)
        detrended = detrend(data, method="linear")
        assert abs(np.mean(detrended)) < 1e-10


# ============================================================
#  运行入口
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
