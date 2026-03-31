import pyuda
import libtokamap
import numpy as np
from typing import override


class PyudaDataSource(libtokamap.DataSource):
    def __init__(self, host: str, port: int, plugin_name: str, function: str = "get"):
        self.host = host
        self.port = port
        self.plugin_name = plugin_name
        self.function = function

        pyuda.Client.server = host
        pyuda.Client.port = port
        self.client = pyuda.Client()

    @override
    def get(self, args: dict[str, str]) -> np.ndarray:
        if 'signal' not in args:
            raise ValueError("signal is required")
        if 'source' not in args:
            raise ValueError("source is required")
        if 'host' not in args:
            raise ValueError("host is required")
        if 'port' not in args:
            raise ValueError("port is required")

        plugin_args = [f'{k}=\"{v}\"' for (k, v) in args.items()]
        request = f'{self.plugin_name}::{self.function}({",".join(plugin_args)})'

        result = self.client.get(request, '')
        return np.asarray(result.data)
