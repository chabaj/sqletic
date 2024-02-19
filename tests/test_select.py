from typing import Iterable
from sqletic import Engine

from sqlton.parser import Table, Column, Operation
from sqlton import parse

class Database:
    def __init__(self, tables: dict[str, Iterable[dict]]):
        self.tables = tables

    def table(self, name:str):
        return self.tables[name]

def test_simple_select():
    statement = "select * from cities"

    database = Database({"cities":({"name": "Prague"}, {"name":"Moulins sur Allier"})})
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)

def test_double_select():
    statement = "select cities.name as city, countries.name as country from cities, countries"

    database = Database({"cities":({"name": "Prague"}, {"name":"Moulins sur Allier"}),
                              "countries":({"name": "Czechia"}, {"name": "France"})})
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)
    
def test_filtered_double_select():
    statement = """
select concat('In ', cities.name, ' city, the spoken language is ', countries.language) as msg
from cities, countries
where cities.country=countries.name
    """

    database = Database({"cities":({"name": "Prague", "country": "Czechia"},
                                   {"name":"Moulins sur Allier", "country": "France"}),
                         "countries":({"name": "Czechia", "language": "Czech"},
                                      {"name": "France", "language": "French"})})
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)

def test_simple_with_inner_join_select():
    statement = """
select concat('In ', cities.name, ' city, the spoken language is ', corresponding_countries.language, ' where ', citizens.name, ' live.')
from cities
     inner join countries as corresponding_countries
           on (cities.country=corresponding_countries.name)
     inner join citizens
           on (cities.name=citizens.city)
    """

    database = Database({"cities":({"name": "Prague", "country": "Czechia"},
                                   {"name":"Moulins sur Allier", "country": "France"}),
                         "countries":({"name": "Czechia", "language": "Czech"},
                                      {"name": "France", "language": "French"}),
                         "citizens":({"name": "Ernest Soucachet", "city": "Moulins sur Allier"},
                                     {"name": "Kvido Bajeux", "city": "Prague"},
                                     {"name": "Zora Bajeux", "city": "Prague"})})
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)

def test_union():
    statement = """
    select name, 'City' from cities
    union
    select name, 'Country' from countries
    union
    select name, 'Citizen' from citizens
    """
    
    engine = Engine(Database({"cities":({"name": "Prague", "country": "Czechia"},
                                        {"name":"Moulins sur Allier", "country": "France"}),
                              "countries":({"name": "Czechia", "language": "Czech"},
                                           {"name": "France", "language": "French"}),
                              "citizens":({"name": "Ernest Soucachet", "city": "Moulins sur Allier"},
                                         {"name": "Kvido Bajeux", "city": "Prague"},
                                         {"name": "Zora Bajeux", "city": "Prague"})}))

    engine.execute(statement)
    
    for entry in engine:
        print(entry, engine.rowcount, engine.description)

def test_intersection():
    statement = """
    select country as Country from cities
    intersect
    select name as Country from countries
    """

    engine = Engine(Database({"cities":({"name": "Prague", "country": "Czechia"},
                                        {"name": "Moulins sur Allier", "country": "France"},
                                        {"name": "Hobbitburg", "country": "Middle-earth"}),
                              "countries":({"name": "Czechia", "language": "Czech"},
                                           {"name": "France", "language": "French"})}))

    engine.execute(statement)
    
    for index, entry in enumerate(engine):
        print(entry, engine.rowcount, engine.description)
    
def test_values():
    statement = "Values('a', 'b', Null)"

    engine = Engine(Database({"cities":({"name": "Prague", "country": "Czechia"},
                                        {"name": "Moulins sur Allier", "country": "France"},
                                        {"name": "Hobbitburg", "country": "Middle-earth"}),
                              "countries":({"name": "Czechia", "language": "Czech"},
                                           {"name": "France", "language": "French"})}))
    
    engine.execute(statement)
    
    for index, entry in enumerate(engine):
        print(entry, engine.rowcount, engine.description)


def test_with():
    statement = """
    WITH RECURSIVE
  works_for_alice(n) AS (
    VALUES('Alice')
    UNION
    SELECT name FROM org, works_for_alice
     WHERE org.boss=works_for_alice.n
  )
SELECT avg(height) FROM org
 WHERE org.name IN works_for_alice
"""

    engine = Engine(Database({"org":[{"name":"Alice", "boss":"Robert"}, {"name":"George", "boss":"Alice"}]}))

    engine.execute(statement)
    
    for index, entry in enumerate(engine):
        print(entry, engine.rowcount, engine.description)
        
def main():
    print("simple_select:")
    test_simple_select()
    print("double_select:")
    test_double_select()
    print("filtered double select:")
    test_filtered_double_select()
    print("test_simple_with_inner_join_select:")
    test_simple_with_inner_join_select()
    print("test_union:")
    test_union()
    print("test_intersection:")
    test_intersection()
    print("test_values:")
    test_values()
    print("test_with:")
    test_with()
