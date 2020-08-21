#!/usr/bin/env python

import argparse
import logging

from .data import create_zarr as zarr_coins
from .utils import download as zarr_download
from .utils import info as zarr_info


def config_logging(loglevel: int, args: argparse.Namespace) -> None:
    loglevel = loglevel - (10 * args.verbose) + (10 * args.quiet)
    logging.basicConfig(level=loglevel)
    # DEBUG logging for s3fs so we can track remote calls
    logging.getLogger("s3fs").setLevel(logging.DEBUG)


def info(args: argparse.Namespace) -> None:
    config_logging(logging.INFO, args)
    zarr_info(args.path)


def download(args: argparse.Namespace) -> None:
    config_logging(logging.WARN, args)
    zarr_download(args.path, args.output, args.name)


def coins(args: argparse.Namespace) -> None:
    config_logging(logging.INFO, args)
    zarr_coins(args.path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase loglevel for each use, e.g. -vvv",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="count",
        default=0,
        help="decrease loglevel for each use, e.q. -qqq",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # info
    parser_info = subparsers.add_parser("info")
    parser_info.add_argument("path")
    parser_info.set_defaults(func=info)

    # download
    parser_download = subparsers.add_parser("download")
    parser_download.add_argument("path")
    parser_download.add_argument("--output", default="")
    parser_download.add_argument("--name", default="")
    parser_download.set_defaults(func=download)

    # coin
    parser_coins = subparsers.add_parser("coins")
    parser_coins.add_argument("path")
    parser_coins.set_defaults(func=coins)

    args = parser.parse_args()
    args.func(args)
