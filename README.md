# tokamunch-pyuda-datasource

![Logo](./docs/logo.png)

Python data source plugin for [tokamunch](https://github.com/stephen-dixon/tokamunch/tree/main).
Fetches data from a UDA server via [pyuda](https://github.com/ukaea/pyuda).

Available on [PyPI](https://pypi.org/project/tokamunch-pyuda-datasource/).

---

## Installation

```sh
pip install tokamunch
pip install tokamunch-pyuda-datasource
```

---

## Configuration

Register the plugin in your tokamunch config file and supply the connection args:

```toml
[data_sources.pyuda]
plugin = "pyuda"

[data_sources.pyuda.args]
host = "localhost"
port = 56565
plugin_name = "uda"
```

| Arg | Type | Description |
|---|---|---|
| `host` | string | UDA server hostname or IP |
| `port` | int | UDA server port |
| `plugin_name` | string | UDA plugin name (e.g. `"uda"`) |

---

## Mapping example

Per-call arguments are passed by the mapping layer for each data request:

```toml
[[mappings]]
id = "ip"
data_source = "pyuda"

[mappings.args]
signal = "AMC_PLASMA CURRENT"
source = "30420"
```

| Arg | Description |
|---|---|
| `signal` | UDA signal name |
| `source` | Shot/pulse number or data source identifier |
| `time` | If present and truthy, returns the time dimension instead of data |

Any additional key/value pairs are passed through as UDA query parameters.

---

## Notes on thread safety

**This plugin is not thread-safe.** `pyuda.Client` stores server and port as class-level
attributes, so concurrent threads sharing a process will interfere with each other.
Use process-based parallelism (e.g. `multiprocessing`) if you need to issue requests
in parallel.

| Property | Value |
|---|---|
| Thread-safe | No |
| Process-safe | Yes |
| Reentrant | No |
| Deterministic | No |
| Cacheable | No |
| Requires network | Yes |

---

## Args: config vs per-call

- **Config args** (`host`, `port`, `plugin_name`) are set once when the plugin is
  constructed from the tokamunch config file.
- **Per-call args** (`signal`, `source`, and any extra UDA query parameters) are
  provided per mapping call by the tokamunch mapping engine.

> **Note:** `host` and `port` are currently also required in per-call args (forwarded
> verbatim to the UDA query string). This duplication is preserved for compatibility
> and may be simplified in a future release.
