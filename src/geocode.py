"""
geocode.py — 地名 → 坐标转换模块

将用户输入的自然语言地名（如"郓城县"）转换为 WGS84 经纬度坐标。
使用离线 GeoJSON 行政区划边界数据，不依赖在线 API。
"""

from pathlib import Path
from shapely.geometry import Point, Polygon, MultiPolygon, box
import geopandas as gpd
import numpy as np


# ---- 数据路径 ----
_BOUNDARY_FILE = Path(__file__).parent.parent / "data" / "raw" / "china_admin.geojson"


def _load_boundary() -> gpd.GeoDataFrame:
    """加载中国行政区划边界数据。

    Returns:
        GeoDataFrame，列：name, admin_level, geometry
    """
    # TODO: 替换为实际的中国县界 GeoJSON 文件
    # 推荐来源: https://github.com/dongli/china-shapefiles
    raise NotImplementedError(
        "请将中国行政区划 GeoJSON 文件放置到: " + str(_BOUNDARY_FILE)
    )


def geocode(region_name: str) -> tuple[float, float, Polygon]:
    """将区域名称解析为经纬度坐标和边界多边形。

    Args:
        region_name: 区域中文名，如 "郓城县"、"济南市"、"山东省"

    Returns:
        (longitude, latitude, boundary_polygon) 元组
        - lon, lat: 区域中心点坐标 (EPSG:4326)
        - boundary: Shapely Polygon，区域边界
    """
    # TODO: 实现地名匹配逻辑
    # 1. 精确匹配
    # 2. 模糊匹配（去掉"省"、"市"、县"后缀）
    raise NotImplementedError("geocode() 待实现")


def get_bounding_box(polygon: Polygon, buffer_km: float = 5.0) -> tuple:
    """根据边界多边形生成带缓冲的矩形范围。

    Args:
        polygon: 区域边界多边形
        buffer_km: 缓冲区半径（公里）

    Returns:
        (min_lon, min_lat, max_lon, max_lat) 矩形范围 (EPSG:4326)
    """
    # 1 度纬度 ≈ 111.32 km
    buffer_deg = buffer_km / 111.32
    minx, miny, maxx, maxy = polygon.bounds
    return (minx - buffer_deg, miny - buffer_deg,
            maxx + buffer_deg, maxy + buffer_deg)
