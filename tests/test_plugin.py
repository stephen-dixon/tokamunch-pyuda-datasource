from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from tokamunch_pyuda_datasource.plugin import PLUGIN_METADATA, create_data_source


def _mock_pyuda_client(monkeypatch):
    mock_client_cls = MagicMock()
    mock_client_instance = MagicMock()
    mock_client_cls.return_value = mock_client_instance
    monkeypatch.setattr("tokamunch_pyuda_datasource.pyuda_data_source.pyuda.Client", mock_client_cls)
    return mock_client_cls, mock_client_instance


VALID_CONFIG = {"host": "localhost", "port": "56565", "plugin_name": "uda"}


def test_create_data_source_returns_datasource(monkeypatch):
    _mock_pyuda_client(monkeypatch)
    ds = create_data_source(VALID_CONFIG)
    assert ds is not None


def test_create_data_source_missing_host():
    with pytest.raises(ValueError, match="host"):
        create_data_source({"port": "56565", "plugin_name": "uda"})


def test_create_data_source_missing_port():
    with pytest.raises(ValueError, match="port"):
        create_data_source({"host": "localhost", "plugin_name": "uda"})


def test_create_data_source_missing_plugin_name():
    with pytest.raises(ValueError, match="plugin_name"):
        create_data_source({"host": "localhost", "port": "56565"})


def test_create_data_source_empty_config():
    with pytest.raises(ValueError):
        create_data_source({})


def test_plugin_metadata_name():
    assert PLUGIN_METADATA.name == "pyuda"


def test_plugin_metadata_not_thread_safe():
    assert PLUGIN_METADATA.thread_safe is False


def test_datasource_get_returns_array(monkeypatch):
    _, mock_client = _mock_pyuda_client(monkeypatch)

    mock_result = MagicMock()
    mock_result.data = np.array([1.0, 2.0, 3.0])
    mock_result.__bool__ = lambda self: True
    mock_client.get.return_value = mock_result

    ds = create_data_source(VALID_CONFIG)
    result = ds.get({"signal": "ip", "source": "30420", "host": "localhost", "port": "56565"})

    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, np.array([1.0, 2.0, 3.0]))


def test_datasource_get_time_dimension(monkeypatch):
    _, mock_client = _mock_pyuda_client(monkeypatch)

    mock_result = MagicMock()
    mock_result.data = np.array([1.0, 2.0])
    mock_result.time.data = np.array([0.0, 0.1])
    mock_result.__bool__ = lambda self: True
    mock_client.get.return_value = mock_result

    ds = create_data_source(VALID_CONFIG)
    result = ds.get({"signal": "ip", "source": "30420", "host": "localhost", "port": "56565", "time": "1"})

    np.testing.assert_array_equal(result, np.array([0.0, 0.1]))


def test_datasource_get_missing_signal(monkeypatch):
    _mock_pyuda_client(monkeypatch)
    ds = create_data_source(VALID_CONFIG)
    with pytest.raises(ValueError, match="signal"):
        ds.get({"source": "30420", "host": "localhost", "port": "56565"})


def test_datasource_get_missing_source(monkeypatch):
    _mock_pyuda_client(monkeypatch)
    ds = create_data_source(VALID_CONFIG)
    with pytest.raises(ValueError, match="source"):
        ds.get({"signal": "ip", "host": "localhost", "port": "56565"})
