from __future__ import annotations

from typing import Any

from tokamunch.plugin_api import DataSourceFactory

from .pyuda_data_source import PyudaDataSource


def create_data_source(args: dict[str, Any]) -> PyudaDataSource:
    required = {"host", "port", "plugin_name"}
    missing = required - args.keys()
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Missing required plugin args: {missing_list}")

    return PyudaDataSource(
        host=args["host"],
        port=int(args["port"]),
        plugin_name=args["plugin_name"],
    )
