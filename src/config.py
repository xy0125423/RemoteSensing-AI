"""
config.py — 配置加载模块

从 YAML 文件加载全局配置，提供默认值回退和路径解析。
"""

from pathlib import Path
import yaml

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def get_default_config() -> dict:
    """返回默认配置（当 config.yaml 缺失或不完整时使用）。"""
    return {
        "time": {"start": "2023-01-01", "end": "2023-12-31"},
        "geo": {"buffer_km": 5, "cloud_max": 20},
        "ndvi": {"scale": 10, "masked_cloud": True, "filter_snow": True},
        "fft": {"window": "hann", "detrend": "linear"},
        "viz": {
            "dpi": 150, "fig_width": 12, "fig_height": 6,
            "cmap": "RdYlGn", "font_family": "SimHei",
        },
        "report": {
            "title": "NDVI 时间序列分析报告",
            "include_fft": True, "include_charts": True,
        },
        "paths": {
            "data_raw": "data/raw", "data_processed": "data/processed",
            "fonts": "data/fonts", "maps": "outputs/maps",
            "charts": "outputs/charts", "reports": "outputs/reports",
            "logs": "logs",
        },
        "logging": {"level": "INFO", "file": "logs/pipeline.log"},
    }


def resolve_paths(cfg: dict) -> dict:
    """将配置中的相对路径转为绝对路径。"""
    for key, rel_path in cfg.get("paths", {}).items():
        abs_path = PROJECT_ROOT / rel_path
        abs_path.mkdir(parents=True, exist_ok=True)
        cfg["paths"][key] = str(abs_path)
    return cfg


def load_config(config_path: str = "config.yaml") -> dict:
    """加载并返回配置字典。

    Args:
        config_path: YAML 配置文件路径（相对于项目根目录或绝对路径）。

    Returns:
        合并了默认值的完整配置字典。
    """
    path = Path(config_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    cfg = get_default_config()

    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            user_cfg = yaml.safe_load(f) or {}
        # 深度合并（简单两层覆盖）
        for section, values in user_cfg.items():
            if isinstance(values, dict) and section in cfg:
                cfg[section].update(values)
            else:
                cfg[section] = values

    cfg = resolve_paths(cfg)
    return cfg
