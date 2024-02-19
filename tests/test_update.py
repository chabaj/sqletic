from typing import Iterable
from sqletic import Engine

class Database:
    def __init__(self, tables: dict[str, Iterable[dict]]):
        self.tables = tables

    def table(self, name:str):
        return self.tables[name]


def test_update():
    database = {"cities":[]}
    engine = Engine(Database(database))
    
    engine.execute("""insert into cities (name, country, planet)
    Values ('Prague', 'Czechia', 'Earth'),
           ('Moulins sur Allier', 'france', 'Earth'),
           ('Paris' , 'france', 'Earth'),
           ('Marseille', 'Franc', 'Earth')""")
    
    engine.execute("""update cities set country='France' where cities.country='france'""")
    
    
    print(database)
    
def test_update_from_select():
    database = {"cities":[{"name":"Corusant", "country":"Coruscant", "planet":"Coruscant"},
                          {"name":"Arrakeen", "country":None, "planet": "Arrakis"},
                          {"name":"Onn", "country":None, "planet": "Arrakis"}],
                "planets":[{"name":"Earth", "fictive":False},
                           {"name":"Arrakis", "fictive":True},
                           {"name":"Coruscant", "fictive":True}]}
    
    engine = Engine(Database(database))
    
    engine.execute("""insert into cities (name, country, planet)
    Values ('Prague', 'Czechia', 'Earth'),
           ('Moulins sur Allier', 'france', 'Earth'),
           ('Paris' , 'france', 'Earth'),
           ('Marseille', 'Franc', 'Earth')""")
    
    engine.execute("""update cities set name=concat('"', cities.name, '"')
                      from planets 
                      where planets.fictive
                            and cities.planet=planets.name
                   """)
    
    
    print(database)

def main():
    print("test_update:")
    test_update()
    print("test_update_from_select:")
    test_update_from_select()

