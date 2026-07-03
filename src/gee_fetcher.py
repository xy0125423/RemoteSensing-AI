"""
gee_fetcher.py — Google Earth Engine 数据获取与导出模块

功能:
    1. 初始化 GEE 连接
    2. 根据区域 + 时间范围筛选 Sentinel-2 影像
    3. 去云处理
    4. 导出 NDVI 波段到本地 GeoTIFF
"""

import ee
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def init_gee(project: str = None) -> None:
    """初始化 Google Earth Engine。

    Args:
        project: GEE Cloud Project ID（可选）
    """
    try:
        ee.Initialize(project=project)
        logger.info("GEE 初始化成功")
    except ee.EEException:
        logger.warning("GEE 未认证，正在启动认证流程...")
        ee.Authenticate()
        ee.Initialize(project=project)
        logger.info("GEE 认证完成并初始化成功")


def mask_s2_clouds(image: ee.Image) -> ee.Image:
    """使用 Sentinel-2 QA60 波段掩膜云像元。

    Args:
        image: Sentinel-2 Level-2A 影像

    Returns:
        去云后的影像（云像元被遮蔽）
    """
    qa60 = image.select("QA60")
    cloud_bit_mask = 1 << 10  # 密集云
    cirrus_bit_mask = 1 << 11  # 卷云
    mask = (
        qa60.bitwiseAnd(cloud_bit_mask).eq(0)
        .And(qa60.bitwiseAnd(cirrus_bit_mask).eq(0))
    )
    return image.updateMask(mask)


def get_s2_collection(
    bbox: tuple,
    start_date: str,
    end_date: str,
    cloud_max: float = 20.0,
) -> ee.ImageCollection:
    """获取 Sentinel-2 影像集合。

    Args:
        bbox: (min_lon, min_lat, max_lon, max_lat) 矩形范围
        start_date: 起始日期 "YYYY-MM-DD"
        end_date: 结束日期 "YYYY-MM-DD"
        cloud_max: 最大云覆盖率 (0-100)

    Returns:
        GEE ImageCollection，已做去云 + NDVI 计算
    """
    region = ee.Geometry.Rectangle(bbox, proj="EPSG:4326", evenOdd=False)

    collection = (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(region)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_max))
        .map(mask_s2_clouds)
    )

    logger.info(
        "Sentinel-2 影像数量: %d (区域=%s, 云量<%.0f%%)",
        collection.size().getInfo(), bbox, cloud_max,
    )

    return collection


def compute_ndvi(image: ee.Image) -> ee.Image:
    """计算单张影像的 NDVI 波段。

    NDVI = (B8 - B4) / (B8 + B4)

    Args:
        image: Sentinel-2 影像

    Returns:
        原始影像 + 新增 'NDVI' 波段
    """
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)


def fetch_and_export(
    collection: ee.ImageCollection,
    output_dir: str,
    scale: int = 10,
) -> list[str]:
    """将 NDVI 影像集合导出到本地 GeoTIFF 文件。

    Args:
        collection: 已计算 NDVI 的 ImageCollection
        output_dir: 输出目录路径
        scale: 像素分辨率（米）

    Returns:
        导出的 GeoTIFF 文件路径列表
    """
    # TODO: 实现批量导出逻辑
    # 方式 A: 逐张导出（适合少量影像）
    # 方式 B: 合成月均 NDVI 后导出（推荐）
    raise NotImplementedError("fetch_and_export() 待实现")
