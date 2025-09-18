import shutil
import pytest
from os import remove, mkdir, path

from guachi.config import DictMatch, OptionConfigurationError

class MockDict(dict):
    pass

def create_configs():
    try:
        if path.exists('/tmp/guachi'):
            shutil.rmtree('/tmp/guachi')
        mkdir('/tmp/guachi')
    except Exception:
        pass

    configs = {
        'conf.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.server_id = 2
guachi.middleware.application = secondary

# Database (Mongo)
guachi.db.host = remote.example.com
guachi.db.port = 00000

# Web Interface
guachi.web.host = web.example.com
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s

# Cache
guachi.cache = 10
""",
        'conf_two.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.application = secondary

# Database (Mongo)
guachi.db.host = remote.example.com
guachi.db.port = 00000

# Web Interface
guachi.web.host = web.example.com
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
guachi.cache = 10
""",
        'conf_three.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.server_id = 2
guachi.middleware.application = secondary

# Database (Mongo)
guachi.db.port = 00000

# Web Interface
guachi.web.host = web.example.com
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
guachi.cache = 10
""",
        'conf_four.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.server_id = 2
guachi.middleware.application = secondary

# Database (Mongo)
guachi.db.host = remote.example.com

# Web Interface
guachi.web.host = web.example.com
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
guachi.cache = 10
""",
        'conf_five.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.server_id = 2

# Database (Mongo)
guachi.db.host = remote.example.com
guachi.db.port = 00000

# Web Interface
guachi.web.host = web.example.com
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
guachi.cache = 10
""",
        'conf_six.ini': """
[DEFAULT]
# Middleware Configuration
guachi.middleware.server_id = 2
guachi.middleware.application = secondary

# Database (Mongo)
guachi.db.host = remote.example.com
guachi.db.port = 00000

# Web Interface
guachi.web.port = 80

# Logging
guachi.log.level = DEBUG
guachi.log.datefmt = %H:%M:%S
guachi.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
guachi.cache = 10
""",
        'conf_seven.ini': """
[DEFAULT]

# Database (Mongo)
guachi.db.host = remote.example.com
guachi.db.port = 0

""",
        'conf_eight.ini': """
[DEFAULT]
# Database (Mongo)
guachi.db.host = example.com 
guachi.db.port = 

# Web Interface
guachi.web.host = 
guachi.web.port = 


""",
        'conf_nine.ini': """
[DEFAULT]
# Database (Mongo)
guachi.db.host = 
guachi.db.port = 

# Web Interface
guachi.web.host = 
guachi.web.port = 

"""
    }

    for fname, text in configs.items():
        with open(f'/tmp/guachi/{fname}', 'w') as txt:
            txt.write(text)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    create_configs()
    yield
    if path.exists('/tmp/guachi'):
        shutil.rmtree('/tmp/guachi')

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

def test_options_config_none_empty_defaults():
    opts = DictMatch()
    actual = opts.options()
    expected = {}
    assert actual == expected

def test_options_config_invalid_empty_defaults():
    opts = DictMatch(config='/path/to/invalid/file')
    actual = opts.options()
    expected = {}
    assert actual == expected

def test_options_config_dict_empty_defaults():
    opts = DictMatch(config={})
    actual = opts.options()
    expected = {}
    assert actual == expected

def test_options_from_dict(mapped_defaults):
    opt = DictMatch(config={}, mapped_defaults=mapped_defaults)
    actual = opt.options()
    expected = mapped_defaults
    assert actual == expected

def test_options_dict_like_object(mapped_defaults):
    mock_dict = MockDict()
    opt = DictMatch(config=mock_dict, mapped_defaults=mapped_defaults)
    actual = opt.options()
    expected = mapped_defaults
    assert actual == expected

def test_options_from_file_empty_options(mapped_options, mapped_defaults):
    opt = DictMatch('/tmp/guachi/conf_nine.ini', mapped_options, mapped_defaults)
    actual = opt.options()
    expected = mapped_defaults
    assert actual == expected

def test_options_from_file_one_option(mapped_options, mapped_defaults):
    opt = DictMatch('/tmp/guachi/conf_eight.ini', mapped_options, mapped_defaults)
    actual = opt.options()
    expected = {
        'db_host': 'example.com',
        'db_port': 27017,
        'web_host': 'localhost',
        'web_port': '8080',
    }
    assert actual == expected

def test_options_from_file_empty_defaults(mapped_options):
    opt = DictMatch('/tmp/guachi/conf_eight.ini', mapped_options, {})
    actual = opt.options()
    expected = {
        'db_host': 'example.com',
        'db_port': '',
        'web_host': '',
        'web_port': '',
    }
    assert actual == expected

def test_options_key_error_passes(mapped_options, mapped_defaults):
    opt = DictMatch('/tmp/guachi/conf_seven.ini', mapped_options, mapped_defaults)
    actual = opt.options()
    expected = {
        'db_host': 'remote.example.com',
        'db_port': '0',
        'web_host': 'localhost',
        'web_port': '8080',
    }
    assert actual == expected

def test_options_from_file_raise_error(mapped_options):
    opt = DictMatch('/tmp/guachi/conf_eight.ini', mapped_options, '')
    with pytest.raises(OptionConfigurationError):
        opt.options()

def test_options_raise_error_mapped_options(mapped_defaults):
    opt = DictMatch('/tmp/guachi/conf_eight.ini', None, mapped_defaults)
    with pytest.raises(OptionConfigurationError):
        opt.options()
