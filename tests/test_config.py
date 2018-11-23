from unittest import mock
import pytest

from prombzex.prombzex import PromBZEx
from prombzex.server import BZServer


def test_empty_config():
    with open('tests/config-empty.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)
    assert bz.servers() == []


def test_defaults_only():
    with open('tests/config-defaults-only.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)
    assert bz.servers() == []
    assert bz.config_get('timeout') == 12345


def test_one_server_no_api_key():
    with open('tests/config-one-server-no-api-key.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)
    assert len(bz.servers()) == 1
    for server_name in bz.servers():
        assert isinstance(server_name, str)
        with pytest.raises(KeyError):
            server = bz.server(server_name)


def test_one_server_no_queries():
    with open('tests/config-one-server-no-queries.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)
    assert len(bz.servers()) == 1
    for server_name in bz.servers():
        assert isinstance(server_name, str)
        server = bz.server(server_name)
        assert bz.config_get('timeout', server_name) == '657483'
        assert server.query_names() == []
