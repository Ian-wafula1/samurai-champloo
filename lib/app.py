#!/usr/bin/env python3
import typer
from utils import seed_db, clear_db
from interfaces import *

app = typer.Typer()
        
@app.command()
def clans():
    ClanInterface.run()

@app.command()
def samurais():
    SamuraiInterface.run()

@app.command()
def weapons():
    WeaponInterface.run()

@app.command()
def quests():
    QuestInterface.run()

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