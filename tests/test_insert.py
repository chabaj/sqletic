from typing import Iterable
from sqletic import Engine

class Database:
    def __init__(self, tables: dict[str, Iterable[dict]]):
        self.tables = tables

    def table(self, name:str):
        return self.tables[name]


def test_insert_from_values():
    statement = """insert into cities (name, country)
    Values ('Prague', 'Czechia'),
           ('Paris', 'France'),
           ('Hobbitburg' , 'Middle-earth'),
           ('Rome', 'Italy')"""

    database = {"cities":[{"name":"Corusant", "country":"Coruscant", "planet":"Coruscant"}]}
    engine = Engine(Database(database))
    
    engine.execute(statement)
    print(database)
    
def test_insert_from_select():
    statement = """insert into countries (name)
    select distinct country as name from cities
    """

    database = {"cities":[{"name":"Corusant", "country":"Coruscant", "planet":"Coruscant"},
                          {"name":"Mos Eisley", "country":"Jabba the hut territory", "planet": "Tatooine"},
                          {"name":"Praha", "country": "Czechia"},
                          {"name":"Brno", "country": "Czechia"},
                          {"name":"Paris", "country": "France"}],
                "countries":[]}
    engine = Engine(Database(database))
    
    engine.execute(statement)
    print(database["countries"])

def main():
    print("test_insert_from_values:")
    test_insert_from_values()
    print("test_insert_from_select:")
    test_insert_from_select()
