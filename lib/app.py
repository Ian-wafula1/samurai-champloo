#!/usr/bin/env python3
import typer
from utils import seed_db, clear_db

app = typer.Typer()

# @app.command()
# def hello(name: str):
#     print(f"Hello {name}")
    
# @app.command()
# def goodbye(name: str, formal: bool = False):
#     if formal:
#         print(f"Goodbye Mr. {name}. Have a good day.")
#     else:
#         print(f"Bye {name}!")
        
@app.command()
def clans():
    pass

@app.command()
def samurais():
    pass

@app.command()
def duels():
    pass

@app.command()
def weapons():
    pass

@app.command()
def quests():
    pass

@app.command()
def seed_database():
    seed_db()
    print('Seeding complete')
    
@app.command()
def clear_database():
    confirm = input('Are you sure you want to clear the database. This will remove all stored data. This action is irreversible!! (y/n)').lower()
    if confirm not in ('y', 'n'):
        print('Wrong input!')
        return
    if confirm == 'n':
        print('Execution cancelled')
    else:
        clear_db()
        print('Database cleared!')
    
if __name__ == '__main__':
    app()