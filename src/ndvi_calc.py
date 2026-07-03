"""
ndvi_calc.py — NDVI 计算与后处理模块

功能:
    1. 从 GeoTIFF 批量读取 NDVI 栅格
    2. 按区域掩膜提取像元值
    3. 统计计算（均值、标准差、有效像元数）
    4. 异常值过滤
"""

import numpy as np
import rasterio
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def read_ndvi_raster(filepath: str) -> np.ndarray:
    """读取单张 NDVI GeoTIFF 文件。

    Args:
        filepath: GeoTIFF 文件路径

    Returns:
        (ndvi_array, transform, crs) 元组
        - ndvi_array: 2D numpy 数组，shape=(H, W)
        - transform: 仿射变换
        - crs: 坐标参考系
    """
    with rasterio.open(filepath) as src:
        data = src.read(1).astype(np.float32)
        # 将无效值 (≤ -9999) 替换为 NaN
        data[data <= -9999] = np.nan
        transform = src.transform
        crs = src.crs
    return data, transform, crs


def mask_by_boundary(
    ndvi_array: np.ndarray,
    transform,
    boundary_geom,
) -> np.ndarray:
    """按行政区划边界掩膜 NDVI 数据。

    Args:
        ndvi_array: 原始 NDVI 2D 数组
        transform: 仿射变换
        boundary_geom: Shapely Polygon/MultiPolygon 边界

    Returns:
        掩膜后的 NDVI 数组（区域外 = NaN）
    """
    # TODO: 用 rasterio.features.geometry_mask 实现
    raise NotImplementedError("mask_by_boundary() 待实现")


def compute_stats(
    ndvi_array: np.ndarray,
    mask_snow: bool = True,
) -> dict:
    """计算单张影像的 NDVI 统计值。

    Args:
        ndvi_array: NDVI 2D 数组
        mask_snow: 是否过滤 NDVI < 0 的积雪像元

    Returns:
        {
            "mean": float,      # 均值
            "std": float,       # 标准差
            "median": float,    # 中位数
            "p95": float,       # 第 95 百分位
            "valid_pixels": int, # 有效像元数
            "total_pixels": int, # 总像元数
            "coverage": float,  # 有效覆盖率 (0-1)
        }
    """
    data = ndvi_array.copy()
    if mask_snow:
        data[data < 0] = np.nan

    valid = data[~np.isnan(data)]
    total = data.size

    return {
        "mean": float(np.nanmean(valid)) if len(valid) > 0 else np.nan,
        "std": float(np.nanstd(valid)) if len(valid) > 0 else np.nan,
        "median": float(np.nanmedian(valid)) if len(valid) > 0 else np.nan,
        "p95": float(np.nanpercentile(valid, 95)) if len(valid) > 0 else np.nan,
        "valid_pixels": len(valid),
        "total_pixels": total,
        "coverage": len(valid) / total if total > 0 else 0,
    }


def batch_compute(
    file_list: list[str],
    dates: list[str],
    output_dir: str,
) -> dict:
    """批量处理 NDVI 影像，导出统计 CSV。

    Args:
        file_list: GeoTIFF 文件路径列表
        dates: 对应的日期列表（等长）
        output_dir: 输出目录

    Returns:
        {"csv_path": str, "stats_list": list[dict], "dates": list[str]}
    """
    # TODO: 实现批量统计 + CSV 导出
    raise NotImplementedError("batch_compute() 待实现")
