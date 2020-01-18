from chalicelib.tododb import TodoDB

def test_id_lookup():
    assert { 'item' : 'buy milk'} == TodoDB().get_todo("1")