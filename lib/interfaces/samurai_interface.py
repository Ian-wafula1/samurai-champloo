from models import Samurai, session
from .samurai_sub_interface import SamuraiSubInterface
from sqlalchemy import desc

class SamuraiInterface:
    
    @staticmethod
    def menu():
        print("""
            0. Exit program
            1. View samurai rankings
            2. Create new samurai
            3. Update existing samurai
            4. Delete samurai
            5. Perform actions on specific samurai""", end='\n\n')
        
    @staticmethod
    def run():
        while True:
            SamuraiInterface.menu()
            inp = input('Select an option: ')
            
            if inp == '0':
                exit()
            
            if inp == '1':
                print('Rank by: \
                    a. Bushido \
                    b. Skill level')
                option = input('Select an option (a/b): ').lower()
                
                if option not in ('a', 'b'):
                    print('Please input the correct choice')
                if option == 'a':
                    samurais = session.query(Samurai).order_by(desc(Samurai.bushido)).all()
                elif option == 'b':
                    samurais = session.query(Samurai).order_by(desc(Samurai.skill_level)).all()
                    
                for i, samurai in enumerate(samurais):
                    print(f"{i+1}. {samurai.details}")
                break
            
            elif inp == '2':
                try:
                    name = input('Enter the samurai\'s name: ')
                    
                    samurai = Samurai(
                        name=name,
                        skill_level = 10
                    )
                    
                    session.add(samurai)
                    session.commit()
                    print(f"Samurai {name} added successfully!")
                    
                    break
                except:
                    print('Kindly input the correct data types.')
                    continue
                    
            elif inp == '3':
                try:
                    id = int(input('Please input the samurai id: '))
                    samurai = session.query(Samurai).filter(Samurai.id == id).first()
                    
                    if not samurai:
                        print('Samurai {id} not found')
                        
                    name = input('Please input the samurai\'s new name: (Input None to retain the name): ')
                    samurai.name = samurai.name if name == 'None' else name
                    bushido = input('Please input the new bushido amount (Input None to retain the name):')
                    if bushido != 'None':
                        print('Nice try lol! Here, we WORK for our bushido. Go do some quests or have some duels, you THIEF!')
                        
                    session.add(samurai)
                    session.commit()
                    print(f'Samurai {id} updated successfully!')
                    break
                    
                except:
                    print('Please input the correct data type.')
                    continue
                
            elif inp == '4':
                try:
                    id = int(input('Enter the id of the samurai you wan\'t to delete: '))
                    samurai = session.query(Samurai).filter(Samurai.id == id).first()
                    
                    if not samurai:
                        print(f"Clan {id} doesn't exist!")
                        continue
                    
                    print(samurai.details)
                    confirm = input('Are you sure you wan\'t to delete this samurai? (y/n)').lower()
                    if confirm not in ('y','n'):
                        print("Please input one of the available choices")
                        continue
                    if confirm == 'n':
                        print('Deletion cancelled!')
                        continue
                    
                    session.delete(samurai)
                    session.commit()
                    print(f'Samurai {id} deleted successfully!')
                    break
                    
                except:
                    print('Please input the correct data type')
                    continue
            elif inp == '5':
                try:
                    id = int(input('Please input the samurai\'s id: '))
                    samurai = session.query(Samurai).filter(Samurai.id == id).first()
                    if not samurai:
                        print(f"Samurai {id} doesn't exist.")
                        continue
                    
                    SamuraiSubInterface.run(id)
                    break
                except:
                    print('Please input the correct data type')
                
            else:
                print('Please input one of the available choices')