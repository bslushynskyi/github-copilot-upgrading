import os
import sqlite3
import pytest
from guachi import database

DB_PATH = '/tmp/test_guachi'

@pytest.fixture(autouse=True)
def cleanup_db():
    yield
    try:
        os.remove(DB_PATH)
    except Exception:
        pass

def test_create_database():
    foo = database.dbdict(DB_PATH)
    assert os.path.isfile(DB_PATH)

def test_init():
    foo = database.dbdict(DB_PATH)
    assert foo.db_filename == DB_PATH
    assert foo.table == '_guachi_data'
    assert foo.select_value == 'SELECT value FROM _guachi_data WHERE key=?'
    assert foo.select_key == 'SELECT key FROM _guachi_data WHERE key=?'
    assert foo.update_value == 'UPDATE _guachi_data SET value=? WHERE key=?'
    assert foo.insert_key_value == 'INSERT INTO _guachi_data (key,value) VALUES (?,?)'
    assert foo.delete_key == 'DELETE FROM _guachi_data WHERE key=?'

def test_init_guachi_table():
    foo = database.dbdict(DB_PATH, table='_guachi_options')
    assert foo.table == '_guachi_options'

def test_get_item_keyerror():
    foo = database.dbdict(DB_PATH)
    with pytest.raises(KeyError):
        foo['meh']

def test_get_item():
    foo = database.dbdict(DB_PATH)
    foo['bar'] = 'beer'
    assert foo['bar'] == 'beer'

def test_setitem_update():
    foo = database.dbdict(DB_PATH)
    foo['a'] = 1
    foo['a'] = 2
    assert foo['a'] == 2

def test_close_db():
    foo = database.dbdict(DB_PATH)
    foo['bar'] = 'beer'
    foo._close()
    with pytest.raises(sqlite3.ProgrammingError):
        foo['bar'] = {'a': 'b'}

def test_setitem_typeerror():
    foo = database.dbdict(DB_PATH)
    with pytest.raises(sqlite3.ProgrammingError):
        foo['bar'] = {'a': 'b'}

def test_delitem_keyerror():
    foo = database.dbdict(DB_PATH)
    with pytest.raises(KeyError):
        del foo['meh']

def test_delitem():
    foo = database.dbdict(DB_PATH)
    foo['bar'] = 'beer'
    assert foo['bar'] == 'beer'
    del foo['bar']
    with pytest.raises(KeyError):
        del foo['bar']

def test_key_empty():
    foo = database.dbdict(DB_PATH)
    assert foo.keys() == []

def test_keys_get_none():
    foo = database.dbdict(DB_PATH)
    assert foo.get('does-not-exist') is None

def test_keys_get_value():
    foo = database.dbdict(DB_PATH)
    foo['bar'] = 'value'
    assert foo.get('bar') == 'value'

def test_keys_get_value_w_default():
    foo = database.dbdict(DB_PATH)
    assert foo.get('foobar', True)

def test_keys():
    foo = database.dbdict(DB_PATH)
    foo['bar'] = 'beer'
    assert foo.keys() == ['bar']

def test_integrity_check_true():
    foo = database.dbdict(DB_PATH)
    assert foo._integrity_check()

# Uncomment to test integrity check false case
# def test_integrity_check_false():
#     with open(DB_PATH, 'w') as foobar:
#         foobar.write('meh')
#     foo = database.dbdict(DB_PATH)
#     assert foo._integrity_check()[0] == 'file is encrypted or is not a database'
