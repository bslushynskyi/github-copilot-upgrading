import os
import pytest

from guachi import ConfigMapper

@pytest.fixture(autouse=True)
def setup_and_teardown_tmp_guachi(tmp_path):
    tmp_guachi = tmp_path / "guachi"
    tmp_guachi.mkdir(exist_ok=True)
    yield
    # Cleanup after test
    for item in tmp_path.iterdir():
        if item.is_dir():
            for subitem in item.iterdir():
                subitem.unlink()
            item.rmdir()
        else:
            item.unlink()

@pytest.fixture
def mapped_options():
    return {
        'guachi.db.host': 'db_host',
        'guachi.db.port': 'db_port',
        'guachi.web.host': 'web_host',
        'guachi.web.port': 'web_port',
    }

@pytest.fixture
def mapped_defaults():
    return {
        'db_host': 'localhost',
        'db_port': 27017,
        'web_host': 'localhost',
        'web_port': '8080',
    }

def test_access_mapped_configs_empty_dict(tmp_path, mapped_options, mapped_defaults):
    config_dir = str(tmp_path / "guachi")
    foo = ConfigMapper(config_dir)
    foo.set_ini_options(mapped_options)
    foo.set_default_options(mapped_defaults)
    foo.set_config({})

    assert foo() == {}
    assert foo.path == f"{config_dir}/guachi.db"
    assert foo.get_ini_options() == {}
    assert foo.get_default_options() == {}
    assert foo.get_dict_config() == mapped_defaults
    assert foo.stored_config() == {}
    assert foo.integrity_check()

def test_access_mapped_configs_dict(tmp_path, mapped_options, mapped_defaults):
    config_dir = str(tmp_path / "guachi")
    foo = ConfigMapper(config_dir)
    foo.set_ini_options(mapped_options)
    foo.set_default_options(mapped_defaults)
    foo.set_config({'db_host': 'example.com', 'db_port': 0})

    expected_config = {
        'web_port': '8080',
        'web_host': 'localhost',
        'db_host': 'example.com',
        'db_port': 0
    }
    assert foo() == {}
    assert foo.path == f"{config_dir}/guachi.db"
    assert foo.get_ini_options() == {}
    assert foo.get_default_options() == {}
    assert foo.get_dict_config() == expected_config
    assert foo.stored_config() == {}
    assert foo.integrity_check()
