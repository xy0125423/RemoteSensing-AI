"""
main.py — 项目入口

用法:
    python main.py --region 郓城县
    python main.py --region 郓城县 --start 2023-01-01 --end 2023-12-31
    python main.py --region 郓城县 --no-report          # 跳过 PDF 报告生成
    python main.py --config config.yaml                  # 指定配置文件
"""

import argparse
import sys
from pathlib import Path

# 将 src 加入路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import load_config
from pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="RemoteSensing-AI: Sentinel-2 NDVI 时间序列分析工具"
    )
    parser.add_argument(
        "--region", type=str, required=True,
        help="目标区域名称，例如：郓城县、济南市"
    )
    parser.add_argument(
        "--start", type=str, default=None,
        help="起始日期 (YYYY-MM-DD)，默认使用 config.yaml 中的值"
    )
    parser.add_argument(
        "--end", type=str, default=None,
        help="结束日期 (YYYY-MM-DD)，默认使用 config.yaml 中的值"
    )
    parser.add_argument(
        "--config", type=str, default="config.yaml",
        help="配置文件路径 (默认: config.yaml)"
    )
    parser.add_argument(
        "--no-report", action="store_true",
        help="跳过 PDF 报告生成"
    )
    parser.add_argument(
        "--skip-fetch", action="store_true",
        help="跳过 GEE 数据获取，仅使用本地已有数据"
    )

    args = parser.parse_args()

    # 加载配置
    cfg = load_config(args.config)

    # 用命令行参数覆盖配置
    if args.start:
        cfg["time"]["start"] = args.start
    if args.end:
        cfg["time"]["end"] = args.end

    # 运行主流程
    run_pipeline(
        region=args.region,
        config=cfg,
        skip_fetch=args.skip_fetch,
        skip_report=args.no_report,
    )


if __name__ == "__main__":
    main()
