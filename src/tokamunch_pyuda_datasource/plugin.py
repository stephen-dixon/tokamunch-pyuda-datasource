from __future__ import annotations

from typing import Any

import libtokamap
from tokamunch import DataSourceFactory, DataSourceMetadata

from .pyuda_data_source import PyudaDataSource

PLUGIN_METADATA = DataSourceMetadata(
    name="pyuda",
    display_name="PyUDA data source",
    description="Fetches data from UDA via pyuda",
    thread_safe=False,  # pyuda.Client uses class-level server/port state
    process_safe=True,
    reentrant=False,
    deterministic=False,
    cacheable=False,
    requires_network=True,
)


# Config args (passed at plugin construction time via tokamunch config):
#   host, port, plugin_name
#
# Per-call args (passed per mapping call):
#   signal, source, and any other UDA query parameters
#
# NOTE: host/port are currently required in both config and per-call args.
# This duplication is preserved for now but may be simplified in a future release.
def create_data_source(args: dict[str, Any]) -> libtokamap.DataSource:
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
