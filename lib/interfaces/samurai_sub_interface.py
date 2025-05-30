from models import Duel, Samurai, Weapon, Quest, session
from sqlalchemy import func, desc

class SamuraiSubInterface:
    
    @staticmethod
    def menu():
        print("0. Exit program \
            1. View details \
            2. Start duel \
            3. View owned weapons \
            4. Buy Weapon \
            5. Sell Weapon \
            6. Join clan \
            7. Leave current clan \
            8. Repair weapon \
            9. Participate in quest \
            10. Mark quest as completed", end='\n\n')
        
    @staticmethod
    def run(id):
        samurai = session.query(Samurai).filter(Samurai.id == id).first()
        if not samurai:
            print(f"Samurai {id} not found!")
            return
        
        while True:
            SamuraiSubInterface.menu()
            inp = input("Select an option: ")

            if inp == '0':
                exit()
                
            elif inp == '1':
                print(samurai.details)
            
            elif inp == '2':
                try:
                    opponent_id = int(input("Enter the opponent's Samurai ID: "))
                    if opponent_id == id:
                        print("You can't duel with yourself!")
                        continue
                    opponent = session.query(Samurai).filter(Samurai.id == opponent_id).first()
                    if not opponent:
                        print("Opponent not found!")
                        continue
                    wager = int(input("Enter the wager: "))
                    location = input("Enter the location: ")
                    duel = Duel(
                        time_held = func.now(),
                        challenger_id=samurai.id, 
                        opponent_id=opponent.id,
                        bushido_wagered = wager,
                        location = location
                    )
                    duel.handle_duel()
                    session.add(duel)
                    session.commit()
                except:
                    print("Invalid input!")
                    
            elif inp == '3':
                weapons = session.query(Weapon).filter(Weapon.samurai_id == id).all()
                for i, weapon in enumerate(weapons):
                    print(f"{i+1}. {weapon.details}")
                
            elif inp == '4':
                try:
                    weapons = session.query(Weapon).filter_by(Weapon.samurai == None).all()
                    for i, weapon in enumerate(weapons):
                        print(f"{i+1}. {weapon.details}")
                    if not weapons:
                        print("No weapons available for purchase!")
                        continue
                    weapon_id = int(input("Enter the weapon's ID: "))
                    print(samurai.purchase_weapon(weapon_id))
                    session.commit()
                    
                except:
                    print('Please input the correct data type')
            
            elif inp == '5':
                weapons = session.query(Weapon).filter(Weapon.samurai_id == id).all()
                for i, weapon in enumerate(weapons):
                    print(f"{i+1}. {weapon.details}")
                if not weapons:
                    print("You don't own any weapons!")
                    continue
                weapon_id = int(input("Enter the weapon's ID: "))
                print(samurai.sell_weapon(weapon_id))
                session.commit()
                
            elif inp == '6':
                try:
                    clan_id = int(input("Enter the clan's ID: "))
                    print(samurai.join_clan(clan_id))
                    session.add(samurai)
                    session.commit()
                except:
                    print('Please input the correct data type')
                
            elif inp == '7':
                print(samurai.leave_clan())
                session.add(samurai)
                session.commit()

            elif inp == '8':
                try:
                    weapons = session.query(Weapon).filter(Weapon.samurai_id == id).all()
                    for i, weapon in enumerate(weapons):
                        print(f"{i+1}. {weapon.details}")
                    if not weapons:
                        print("You don't own any weapons!")
                        continue
                    weapon_id = int(input("Enter the weapon's ID: "))
                    print(samurai.repair_weapon(weapon_id))
                    session.commit()
                except:
                    print('Please input the correct data type')
                
            elif inp == '9':
                try:
                    quests = session.query(Quest).order_by(desc(Quest.difficulty)).all()
                    for i, quest in enumerate(quests):
                        print(f"{i+1}. {quest.details}")
                    if not quests:
                        print("No quests available!")
                        continue
                    quest_id = int(input("Enter the quest's ID: "))
                    print(Quest.assign_quest(quest_id, samurai.id))
                    session.commit()
                except:
                    print('Please input the correct data type')
                    
            elif inp =='10':
                try:
                    quests = session.query(Quest).filter(Quest.samurais.contains(samurai)).all()
                    if not quests:
                        print("You are not part of any quests!")
                        continue
                    for i, quest in enumerate(quests):
                        print(f"{i+1}. {quest.details}")
                    quest_id = int(input("Enter the quest's ID: "))
                    print(Quest.complete_quest(quest_id))
                    session.commit()
                except:
                    print('Please input the correct data type')
            
            else:
                print("Invalid input. Please try again.")
                
            
        