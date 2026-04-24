import pyuda
import libtokamap
import numpy as np
from typing_extensions import override
import logging
import time


logger = logging.getLogger(__name__)


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
            logging.error("signal is required")
            raise ValueError("signal is required")
        if 'source' not in args:
            logging.error("source is required")
            raise ValueError("source is required")
        if 'host' not in args:
            logging.error("host is required")
            raise ValueError("host is required")
        if 'port' not in args:
            logging.error("port is required")
            raise ValueError("port is required")


        plugin_args = [f'{k}=\"{v}\"' for (k, v) in args.items()]
        request = f'{self.plugin_name}::{self.function}({",".join(plugin_args)})'

        logger.debug("Pyuda request: %s", request)

        t0 = time.perf_counter()
        result = self.client.get(request, '')
        dt = time.perf_counter() - t0

        if result:
            logger.debug(f"Pyuda result for signal {args['signal']}: \n"
                         f"\tname: {result.label}\n"
                         f"\ttype: {result.data.dtype}\n"
                         f"\tshape: {result.data.shape}\n"
                         f"\tsize: {result.data.size}\n"
                         f"\tdims: {result.dims}\n"
                         f"\ttime: {dt}")
        else:
            logger.debug(f"No data returned for signal {args['signal']}")

        if "time" in args and args["time"]:
            return np.asarray(result.time.data)
        if "error" in args and args["error"]:
            return np.asarray(result.error.data)

        return np.asarray(result.data)
