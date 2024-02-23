from sqletic import Filter
from sqlton.parser import Table, Column, Operation
from sqlton import parse

def test_value():
    result = Filter({})(5)
    assert 5 == result

def test_column():
    result = Filter({'realm':{'Gobelin':'troll'}})(Column('Gobelin'))
    assert 'troll' == result

def test_table_column():
    result = Filter({'realm':{'Gobelin':'lol'}})(Column('Gobelin', Table('realm')))
    assert 'lol' == result

def test_add():
    result = Filter({'realm':{'Gobelin':'lol'}})(Operation(('PLUS',), 5, 10))
    assert 15 == result

def test_substract():
    result = Filter({'realm':{'Gobelin':'lol'}})(Operation(('MINUS',), 5, 10))
    assert -5 == result

def test_multplication():
    result = Filter({'realm':{'Gobelin':'lol'}})(Operation(('MULTIPLICATION',), 5, 10))
    assert 50 == result

def test_column():
    result = Filter({'realm':{'Gobelin':66.6}})(Operation(('MULTIPLICATION',), 10, Column('Gobelin')))
    assert 666 == result, f"expected {666} got {result}"

def test_parse():
    statement = parse('select (5 * 6) = realm.Gobelin from realm')
    scope = {'realm':{'Gobelin':30}}
    result = Filter(scope)(statement.select_core.result_column_list[0])
    assert result
    
def main():
    test_value()
    test_column()
    test_table_column()
    test_add()
    test_substract()
    test_multplication()
    test_parse()
