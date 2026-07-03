"""
pipeline.py — 主流程编排模块

将所有处理步骤串联：地名解析 → 数据获取 → NDVI 计算
→ 时间序列分析 → FFT 频谱分析 → 可视化 → 报告生成

这是整个项目的工作流大脑。
"""

import logging
import time
from pathlib import Path

from config import PROJECT_ROOT
from geocode import geocode, get_bounding_box
from gee_fetcher import init_gee, get_s2_collection, compute_ndvi, fetch_and_export
from ndvi_calc import read_ndvi_raster, batch_compute
from timeseries import build_timeseries, interpolate_gaps, smooth_savgol
from fft_analyzer import apply_window, detrend, compute_fft, find_dominant_periods
from visualizer import set_font, plot_timeseries, plot_fft_spectrum
from report_gen import generate_pdf_report

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO", log_file: str = None) -> None:
    """配置日志系统。"""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8") if log_file else logging.NullHandler(),
        ],
    )


def run_pipeline(
    region: str,
    config: dict,
    skip_fetch: bool = False,
    skip_report: bool = False,
) -> dict:
    """执行完整的 NDVI 时间序列分析流程。

    Args:
        region: 目标区域名 (如 "郓城县")
        config: 配置字典 (来自 load_config())
        skip_fetch: 跳过 GEE 数据获取 (仅使用本地数据)
        skip_report: 跳过 PDF 报告生成

    Returns:
        包含所有中间结果的字典
    """
    # ---- 0. 初始化 ----
    t0 = time.time()
    log_cfg = config.get("logging", {})
    setup_logging(
        level=log_cfg.get("level", "INFO"),
        log_file=config.get("paths", {}).get("logs", "logs") + "/pipeline.log",
    )
    logger.info("=" * 60)
    logger.info("RemoteSensing-AI 流程启动")
    logger.info("目标区域: %s", region)
    logger.info("=" * 60)

    results = {"region": region, "status": "running"}

    # ---- 1. 地名解析 ----
    logger.info("Step 1/7: 地名解析...")
    lon, lat, boundary = geocode(region)
    bbox = get_bounding_box(boundary, config["geo"]["buffer_km"])
    results["lon"], results["lat"] = lon, lat
    results["bbox"] = bbox

    # ---- 2. GEE 数据获取 ----
    if not skip_fetch:
        logger.info("Step 2/7: GEE 数据获取...")
        init_gee()
        collection = get_s2_collection(
            bbox,
            config["time"]["start"],
            config["time"]["end"],
            config["geo"]["cloud_max"],
        )
        collection = collection.map(compute_ndvi)
        tif_files = fetch_and_export(
            collection,
            config["paths"]["data_raw"],
            config["ndvi"]["scale"],
        )
        results["tif_files"] = tif_files
    else:
        logger.info("Step 2/7: 跳过 GEE 获取 (--skip-fetch)")

    # ---- 3. NDVI 批量计算 ----
    logger.info("Step 3/7: NDVI 批量计算...")
    # TODO: 从 tif_files 读取并计算统计值

    # ---- 4. 时间序列构建 ----
    logger.info("Step 4/7: 时间序列构建...")
    # TODO: 从统计值构建时间序列，插值 + 平滑

    # ---- 5. FFT 频谱分析 ----
    logger.info("Step 5/7: FFT 频谱分析...")
    # TODO: 对平滑后的序列做 FFT，提取主周期

    # ---- 6. 可视化 ----
    logger.info("Step 6/7: 可视化...")
    set_font()
    # TODO: 调用 visualizer 生成地图 + 图表

    # ---- 7. 报告生成 ----
    if not skip_report:
        logger.info("Step 7/7: PDF 报告生成...")
        # TODO: 调用 report_gen 生成最终报告
    else:
        logger.info("Step 7/7: 跳过报告生成 (--no-report)")

    # ---- 完成 ----
    elapsed = time.time() - t0
    logger.info("流程完成 ✅ 总耗时: %.1f 秒", elapsed)
    results["status"] = "completed"
    results["elapsed_seconds"] = elapsed
    return results
