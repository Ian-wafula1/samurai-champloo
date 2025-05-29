from models import Clan, Samurai, session
from sqlalchemy import desc

class ClanInterface:
    
    @staticmethod
    def menu():
        print("0. Exit program \
            1. View clan rankings \
            2. Create new clan \
            3. Update existing clan \
            4. Delete clan ", end='\n\n')
        
    @staticmethod
    def run():
        
        while True:
            ClanInterface.menu()
            inp = input('Select an option: ')
            
            if inp == '0':
                exit()
            
            if inp == '1':
                clans = session.query(Clan).order_by(desc(Clan.clan_bushido_total)).all()
                for i, clan in enumerate(clans):
                    print(f"{i+1}. {clan.details}")
                break
            
            elif inp == '2':
                try:
                    name = input('Enter the clan\'s name: ')
                    dojo = input("Enter the clan dojo's name: ")
                    leader = input("Enter the id of the clan's leader (Must be an existing samurai without a clan): ")
                    samurai = session.query(Samurai).filter(Samurai.id == leader).first()
                    
                    if not samurai:
                        print(f'Samurai {leader} does not exist. Please try again')
                        continue
                    if samurai.clan:
                        print(f"Samurai {leader} already belongs to a clan. The samurai must quit their clan before forming a new one")
                        continue
                    
                    clan = Clan(
                        name = name,
                        dojo = dojo,
                        leader_id = int(leader)
                    )
                    
                    session.add(clan)
                    session.commit()
                    print(f"Clan {name} added successfully!")
                    
                    break
                except:
                    print('Kindly input the correct data types.')
                    continue
                    
            elif inp == '3':
                try:
                    id = int(input('Please input the clan id: '))
                    clan = session.query(Clan).filter(Clan.id == id).first()
                    if not clan:
                        print('Clan {id} not found')
                    name = input('Please input the new clan name (Input None to retain the name): ')
                    clan.name = clan.name if name=='None' else name
                    dojo = input('Please input the new dojo\'s name (Input None to retain the dojo): ')
                    clan.dojo = clan.dojo if dojo == 'None' else dojo
                    leader = input('Please input the new leader\'s id (Input None to retain the name): ')
                    if leader != 'None':
                        samurai = session.query(Samurai).filter(Samurai.id == leader).first()
                        if not samurai:
                            print(f'Samurai {leader} does not exist. Please try again')
                            continue
                        if samurai not in clan.samurais:
                            print(f"Samurai {leader} is not a member of the clan. The samurai must join the clan in order to become the clan leader.")
                            continue
                        clan.leader_id = leader
                        
                    session.add(clan)
                    session.commit()
                    print(f'Clan {id} updated successfully!')
                    break
                    
                except:
                    print('Please input the correct data type.')
                    continue
                
            elif inp == '4':
                try:
                    id = int(input('Enter the id of the clan you wan\'t to delete: '))
                    clan = session.query(Clan).filter(Clan.id == id).first()
                    if not clan:
                        print(f"Clan {id} doesn't exist!")
                        continue
                    print(clan.details)
                    confirm = input('Are you sure you wan\'t to delete this clan? (y/n): ').lower()
                    if confirm not in ('y','n'):
                        raise Exception()
                    if confirm == 'n':
                        print('Deletion cancelled!')
                        continue
                    clan.delete()
                    session.commit()
                    print(f'Clan {id} deleted successfully!')
                    break
                    
                except:
                    print('Please input the correct data type')
                    continue
                
            else:
                print('Please input one of the available choices')