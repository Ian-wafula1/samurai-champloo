from models import Weapon, session

class WeaponInterface:
    
    @staticmethod
    def menu():
        print("0. Exit the program \
            1. View all weapons \
            2. View weapons available for purchase \
            3. Add weapon \
            4. Update existing weapon \
            5. Delete weapon", end='\n\n')
        
    @staticmethod
    def run():
        while True:
            WeaponInterface.menu()
            inp = input('Select an option: ')
            
            if inp == '0':
                exit()
            
            if inp == '1':
                weapons = session.query(Weapon).all()
                for i, weapon in enumerate(weapons):
                    print(f"{i+1}. {weapon.details} | Owner: {weapon.samurai.name}")
                break
            
            elif inp == '2':
                weapons = session.query(Weapon).filter_by(Weapon.samurai == None).all()
                for i, weapon in enumerate(weapons):
                    print(f"{i+1}. {weapon.details}")
                break
            elif inp == '3':
                try:
                    name = input("Enter the weapon's name: ")
                    type = input("Enter the weapon's type: ")
                    damage = int(input("Enter the weapon's damage: "))
                    cost = int(input("Enter the weapon's cost: "))
                    
                    weapon = Weapon(
                        name = name,
                        type = type,
                        damage = damage,
                        bushido_cost = cost
                    )
                    session.add(weapon)
                    session.commit()
                    
                    print('Weapon added successfully!')
                    break
                    
                except:
                    print('Please input the correct data type.')
                    continue
            
            elif inp == '4':
                try:
                    id = int(input("Enter the id of the weapon you want to update: "))
                    weapon = session.query(Weapon).filter(Weapon.id == id).first()
                    if not weapon:
                        print(f"Weapon {id} doesn't exist!")
                        continue
                    
                    name = input("Enter the weapon's name (Input None to retain the name): ")
                    weapon.name = weapon.name if name == 'None' else name
                    type = input("Enter the weapon's type (Input None to retain the name): ")
                    weapon.type = weapon.name if type == 'None' else type
                    damage = input("Enter the weapon's damage (Input None to retain the name): ")
                    weapon.damage = weapon.name if damage == 'None' else damage
                    bushido_cost = input("Enter the weapon's bushido_cost (Input None to retain the name): ")
                    weapon.bushido_cost = weapon.name if bushido_cost == 'None' else bushido_cost
                    
                    session.add(weapon)
                    session.commit()
                    print(f"Weapon {id} updated successfully!")
                    break
                
                except:
                    print('Please input the correct data type.')
                    continue
                
            elif inp == '5':
                try:
                    id = int(input('Enter the id of the weapon you want to delete: '))
                    weapon = session.query(Weapon).filter(Weapon.id == id).first()
                    if not weapon:
                        print(f"Weapon {id} doesn't exist!")
                        continue
                    
                    print(weapon.details)
                    confirm = input('Are you sure you wan\'t to delete this weapon? (y/n): ').lower()
                    if confirm not in ('y','n'):
                        raise Exception()
                    if confirm == 'n':
                        print('Deletion cancelled!')
                        continue
                    if weapon.samurai:
                        owner = weapon.samurai
                        owner.bushido += int(0.8 * weapon.bushido_cost)
                        print(f"The weapon's owner, samurai {owner.name} has been compensated with 80% of the weapon's cost.")
                        session.add(owner)
                        session.commit()
                    weapon.delete()
                    session.commit()
                    print(f'Weapon {id} deleted successfully!')
                    break
                    
                except:
                    print('Please input the correct data type')
                    continue
                
            else:
                print('Please input one of the available choices')