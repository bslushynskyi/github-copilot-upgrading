import os
import pytest

from guachi import ConfigMapper
from guachi.database import dbdict

DEFAULT_CONFIG = {
    'frequency': 60,
    'master': 'False',
    'host': 'localhost',
    'ssh_user': 'root',
    'ssh_port': 22,
    'hosts_path': '/opt/pacha',
    'hg_autocorrect': 'True',
    'log_enable': 'False',
    'log_path': 'False',
    'log_level': 'DEBUG',
    'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
    'log_datefmt': '%H:%M:%S'
}

@pytest.fixture(autouse=True)
def cleanup_files():
    for path in ['/tmp/guachi.db', '/tmp/foo_guachi.db']:
        try:
            os.remove(path)
        except Exception:
            pass
    yield
    for path in ['/tmp/guachi.db', '/tmp/foo_guachi.db']:
        try:
            os.remove(path)
        except Exception:
            pass

def test_init():
    foo = ConfigMapper('/tmp')
    assert foo.path == '/tmp/guachi.db'

def test__call__():
    foo = ConfigMapper('/tmp')
    assert foo() == {}

def test_set_ini_options():
    foo = ConfigMapper('/tmp')
    my_config = {'config.db.port': 'db_port'}
    foo.set_ini_options(my_config)
    db = dbdict(path='/tmp/guachi.db', table='_guachi_options')
    assert db.get_all() == my_config

def test_set_default_options():
    foo = ConfigMapper('/tmp')
    my_config = {'db_port': 1234}
    foo.set_default_options(my_config)
    db = dbdict(path='/tmp/guachi.db', table='_guachi_defaults')
    assert db.get_all() == my_config

def test_get_ini_options():
    foo = ConfigMapper('/tmp')
    my_config = {'config.db.port': 'db_port'}
    foo.set_ini_options(my_config)
    defaults = foo.get_ini_options()
    assert defaults['config.db.port'] == 'db_port'

def test_get_default_options():
    foo = ConfigMapper('/tmp')
    my_config = {'db_port': 1234}
    foo.set_default_options(my_config)
    defaults = foo.get_default_options()
    assert defaults['db_port'] == 1234

def test_path_verify_file():
    foo = ConfigMapper('/tmp/foo_guachi.db')
    assert foo._path_verify('/tmp/foo_guachi.db') == '/tmp/foo_guachi.db'

def test_path_verify_dir():
    foo = ConfigMapper('/tmp')
    assert foo._path_verify('/tmp') == '/tmp/guachi.db'

def test_update_config_dict_empty():
    foo = ConfigMapper('/tmp')
    foo.update_config({})
    db = dbdict('/tmp/guachi.db')
    assert db.get_all() == {}

def test_update_config_dict():
    foo = ConfigMapper('/tmp')
    foo.update_config(DEFAULT_CONFIG)
    db = dbdict('/tmp/guachi.db')
    assert db.get_all() == DEFAULT_CONFIG

def test_set_config_dict_empty():
    foo = ConfigMapper('/tmp')
    foo.set_config({})
    db = dbdict('/tmp/guachi.db')
    assert db.get_all() == {}

def test_set_config_dict():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    db = dbdict('/tmp/guachi.db')
    assert db.get_all() == DEFAULT_CONFIG

def test_get_dict_config():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    assert foo.get_dict_config() == DEFAULT_CONFIG

def test_integrity_check():
    foo = ConfigMapper('/tmp')
    foo.set_config(DEFAULT_CONFIG)
    assert foo.integrity_check()

def test_stored():
    foo = ConfigMapper('/tmp')
    bar = foo.stored_config()
    assert bar == {}

def test_stored_get_data():
    foo = ConfigMapper('/tmp')
    bar = foo.stored_config()
    bar['a'] = 1
    assert bar == {'a': 1}
