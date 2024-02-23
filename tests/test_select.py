from typing import Iterable
from sqletic import Engine

from sqlton.parser import Table, Column, Operation
from sqlton import parse

def test_simple_select():
    statement = "select * from cities"

    database = {"cities":({"name": "Prague"}, {"name":"Paris"})}
    engine = Engine(database)
    engine.execute(statement)
    
    for entry in engine:
        print(entry)

def test_double_select():
    statement = "select cities.name as city, countries.name as country from cities, countries"

    database = {"cities":({"name": "Prague"}, {"name":"Paris"}),
                "countries":({"name": "Czechia"}, {"name": "France"})}
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

    database = {"cities":({"name": "Prague", "country": "Czechia"},
                          {"name":"Paris", "country": "France"}),
                "countries":({"name": "Czechia", "language": "Czech"},
                             {"name": "France", "language": "French"})}
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

    database = {"cities":({"name": "Prague", "country": "Czechia"},
                          {"name": "Cesky Krumlov", "country": "Czechia"},
                          {"name":"Paris", "country": "France"}),
                "countries":({"name": "Czechia", "language": "Czech"},
                             {"name": "France", "language": "French"}),
                "citizens":({"name": "Pablo Picasso", "city": "Paris"},
                            {"name": "Alfons Mucha", "city": "Prague"},
                            {"name": "Egon Schiele", "city": "Cesky Krumlov"})}
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
    
    engine = Engine({"cities":({"name": "Prague", "country": "Czechia"},
                                        {"name":"Paris", "country": "France"}),
                              "countries":({"name": "Czechia", "language": "Czech"},
                                           {"name": "France", "language": "French"}),
                              "citizens":({"name": "Auguste Renoir", "city": "Paris"},
                                         {"name": "Alfons Mucha", "city": "Prague"},
                                         {"name": "Jiri Manes", "city": "Prague"})})

    engine.execute(statement)
    
    for entry in engine:
        print(entry, engine.rowcount, engine.description)

def test_intersection():
    statement = """
    select country as Country from cities
    intersect
    select name as Country from countries
    """

    engine = Engine({"cities":({"name": "Prague", "country": "Czechia"},
                                        {"name": "Moulins sur Allier", "country": "France"},
                                        {"name": "Hobbitburg", "country": "Middle-earth"}),
                              "countries":({"name": "Czechia", "language": "Czech"},
                                           {"name": "France", "language": "French"})})

    engine.execute(statement)
    
    for index, entry in enumerate(engine):
        print(entry, engine.rowcount, engine.description)
    
def test_values():
    statement = "Values('a', 'b', Null)"

    engine = Engine({"cities":({"name": "Prague", "country": "Czechia"},
                               {"name": "Moulins sur Allier", "country": "France"},
                               {"name": "Hobbitburg", "country": "Middle-earth"}),
                     "countries":({"name": "Czechia", "language": "Czech"},
                                  {"name": "France", "language": "French"})})
    
    engine.execute(statement)
    
    for index, entry in enumerate(engine):
        print(entry, engine.rowcount, engine.description)


def test_with():
    statement = """
WITH RECURSIVE
knows_alice(name) AS (
         VALUES('Alice')
    UNION
         SELECT name
         FROM org, knows_alice
         WHERE org.boss=knows_alice.name
    )
SELECT name FROM knows_alice
"""

    engine = Engine({"org":[{"name":"Robert", "boss":None},
                            {"name":"Michael", "boss":"Robert"},
                            {"name":"Alice", "boss":"Robert"},
                            {"name":"George", "boss":"Alice"},
                            {"name":"Alan", "boss":"Alice"},
                            {"name":"John", "boss":"Alan"}],
                     "family":[{"name":"Adam", "relative":"Alice"},
                               {"name":"Zachary", "relative":"Alan"},
                               {"name":"Alice", "relative":"Zachary"},
                               {"name":"Alan", "relative":"Alan"}]})

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
