from models import Quest, Samurai, session
from sqlalchemy import desc

class QuestInterface:

    @staticmethod
    def menu():
        print("""
        0. Exit program
        1. View all quests
        2. Create new quest
        3. Update existing quest
        4. Delete quest
        5. View details of specific quest
        6. View participating samurais of specific quest
        """, end='\n\n')

    @staticmethod
    def run():
        while True:
            QuestInterface.menu()
            inp = input('Select an option: ')

            if inp == '0':
                exit()

            if inp == '1':
                quests = session.query(Quest).all()
                difficulties = ['Easy', 'Medium', 'Hard', 'Legendary']
                
                quests.sort(key=lambda x: difficulties.index(x.difficulty_rating), reverse=True)
                for i, quest in enumerate(quests):
                    print(f"{i+1}. {quest.details}", end='\n\n')
                break
            
            elif inp == '2':
                try:
                    name = input("Enter quest name: ")
                    description = input("Enter quest description: ")
                    type = input("Enter quest type: ")
                    difficulty = input("Enter quest difficulty (Easy/Medium/Hard/Legendary): ")
                    
                    if difficulty not in ('Easy', 'Medium', 'Hard', 'Legendary'):
                        print("Kindly input the correct difficulty")
                        continue
                    
                    bushido_reward = int(input("Enter bushido reward: "))

                    quest = Quest(
                        name=name,
                        description=description,
                        type=type,
                        difficulty_rating=difficulty,
                        bushido_reward=bushido_reward,
                        status = 'pending'
                    )

                    session.add(quest)
                    session.commit()
                    print(f"Quest '{name}' added successfully!")
                    break

                except:
                    print("Kindly input the correct data types.")
                    continue

            elif inp == '3':
                try:
                    id = int(input("Please input the quest ID: "))
                    quest = session.query(Quest).filter(Quest.id == id).first()
                    if not quest:
                        print(f"Quest {id} not found")
                        continue
                    
                    print(quest.details)
                    name = input("Enter new quest name (or None to keep): ")
                    quest.name = quest.name if name == 'None' else name

                    description = input("Enter new description (or None to keep): ")
                    quest.description = quest.description if description == 'None' else description

                    q_type = input("Enter new type (or None to keep): ")
                    quest.type = quest.type if q_type == 'None' else q_type

                    difficulty = input("Enter new difficulty (or None to keep): ")
                    quest.difficulty_rating = quest.difficulty_rating if difficulty == 'None' else difficulty

                    reward = input("Enter new bushido reward (or None to keep): ")
                    quest.bushido_reward = quest.bushido_reward if reward == 'None' else int(reward)

                    session.add(quest)
                    session.commit()
                    print(f"Quest {id} updated successfully!")
                    break

                except:
                    print("Please input the correct data type.")
                    continue

            elif inp == '4':
                try:
                    id = int(input("Enter the ID of the quest to delete: "))
                    quest = session.query(Quest).filter(Quest.id == id).first()
                    if not quest:
                        print(f"Quest {id} doesn't exist!")
                        continue

                    print(quest.details)
                    confirm = input("Are you sure you want to delete this quest? (y/n): ").lower()
                    if confirm not in ('y', 'n'):
                        raise Exception()
                    if confirm == 'n':
                        print("Deletion cancelled!")
                        continue

                    session.delete(quest)
                    session.commit()
                    print(f"Quest {id} deleted successfully!")
                    break

                except:
                    print("Please input the correct data type")
                    continue

            elif inp == '5':
                try:
                    id = int(input("Enter the ID of the quest: "))
                    quest = session.query(Quest).filter(Quest.id == id).first()
                    if not quest:
                        print(f"Quest {id} doesn't exist!")
                        continue

                    print(quest.details)
                    break

                except:
                    print("Please input the correct data type")
                    continue
            
            elif inp == '6':
                try:
                    id = int(input("Enter the ID of the quest: "))
                    quest = session.query(Quest).filter(Quest.id == id).first()
                    
                    if not quest:
                        print(f"Quest {id} doesn't exist!")
                        continue
                    
                    if not quest.samurais:
                        print(f"Quest {id} has no participants")
                        continue
                    
                    print(f"Participants of quest {id}:")
                    for samurai in quest.samurais:
                        print(samurai.details)
                    break

                except:
                    print("Please input the correct data type")
                    continue
            else:
                print("Please input one of the available choices")
