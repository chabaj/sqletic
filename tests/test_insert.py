from typing import Iterable
from sqletic import Engine

def test_insert_from_values():
    statement = """insert into cities (name, country)
    Values ('Prague', 'Czechia'),
           ('Paris', 'France'),
           ('Hobbitburg' , 'Middle-earth'),
           ('Rome', 'Italy')"""

    engine = Engine({"cities":[{"name":"Corusant", "country":"Coruscant", "planet":"Coruscant"}]})
    
    engine.execute(statement)
    print(engine.tables)
    
def test_insert_from_select():
    statement = """insert into countries (name)
    select distinct country as name from cities
    """

    engine = Engine({"cities":[{"name":"Corusant", "country":"Coruscant", "planet":"Coruscant"},
                               {"name":"Mos Eisley", "country":"Jabba the hut territory", "planet": "Tatooine"},
                               {"name":"Praha", "country": "Czechia"},
                               {"name":"Brno", "country": "Czechia"},
                               {"name":"Paris", "country": "France"}],
                     "countries":[]})
    
    engine.execute(statement)
    print(engine.tables["countries"])

def main():
    print("test_insert_from_values:")
    test_insert_from_values()
    print("test_insert_from_select:")
    test_insert_from_select()
