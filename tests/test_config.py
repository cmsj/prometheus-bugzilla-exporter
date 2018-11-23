from unittest import mock
import pytest

from prombzex.prombzex import PromBZEx
from prombzex.server import BZServer
from simple_rest_client.models import Response


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


def test_server_query_simple_counter(monkeypatch):
    def mock_search_return(params=None):
        assert params['test1'] == 'test2'
        return Response(status_code=200,
                        url='',
                        method='GET',
                        headers={},
                        client_response=None,
                        body={"bugs": [{}, {}]})

    with open('tests/config-one-server-one-query.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)
    assert len(bz.servers()) == 1
    for server_name in bz.servers():
        assert isinstance(server_name, str)
        server = bz.server(server_name)
        monkeypatch.setattr(server.bugzilla.bz, 'search', mock_search_return)
        with pytest.raises(KeyError):
            server.run_query('non-existant query')
        for query_name in server.query_names():
            output = server.run_query(query_name)
            assert output == """# HELP simple_counter_test Help for simple_counter_test
# TYPE simple_counter_test counter
simple_counter_test 2
"""


def test_server_fail(monkeypatch):
    def mock_search_return(params=None):
        return Response(status_code=401,
                        url='',
                        method='GET',
                        headers={},
                        client_response=None,
                        body={})

    with open('tests/config-one-server-one-query.json', 'r') as filep:
        bz = PromBZEx(filep)
        server = bz.server(bz.servers()[0])
        monkeypatch.setattr(server.bugzilla.bz, 'search', mock_search_return)
        with pytest.raises(ValueError):
            server.run_query('simple_counter_test')


def test_output_writing(monkeypatch):
    import os
    import tempfile
    tempp, tmp_output_filename = tempfile.mkstemp()

    def mock_path_join(path, *paths):
        return tmp_output_filename

    with open('tests/config-one-server-one-query.json', 'r') as filep:
        bz = PromBZEx(filep)
    assert isinstance(bz, PromBZEx)

    test_output = "test1234"
    with monkeypatch.context() as m:
        m.setattr(os.path, 'join', mock_path_join)
        bz.write(test_output)
        bz.write(test_output, bz.servers()[0])

    with open(tmp_output_filename, 'r') as outp:
        written_output = outp.read()

    assert written_output == test_output
    os.remove(tmp_output_filename)
