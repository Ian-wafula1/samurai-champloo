from . import data
from .clear import clear_db
import random
from models import Samurai, Clan, Weapon, Quest, session

def seed_db():
    
    clear_db()
    
    samurais = [Samurai(
        name = data.samurai_names[i],
        skill_level = random.randint(20, 75),
        bushido= random.randint(25, 60),
    ) for i in range(36)]
    
    session.add_all(samurais)
    session.commit()
    
    
    weapons = [Weapon(
        name = weapon[0],
        type = weapon[1],
        damage = random.randint(20, 50),
        durability = 100,
        bushido_cost = random.randint(20,40)
    ) for weapon in data.weapons]
    
    session.add_all(weapons)
    session.commit()
    
    
    clans = []
    for i in range(len(data.clan_names)):
        clan = Clan(
            name = data.clan_names[i],
            dojo = data.dojos[i],
            leader_id = samurais[i].id
        )
        samurais[i].clan = clan
        clans.append(clan)
        
    session.add_all(clans)
    session.add_all(samurais)
    session.commit()
    
    
    quests = [Quest(
        name = data.quest_names[i],
        description = random.choice(data.quest_descriptions),
        type = random.choice(data.quest_types),
        difficulty_rating = random.choice('Easy/Medium/Hard/Legendary'.split('/')),
        bushido_reward = random.randint(50, 150),
        status = "pending"
    ) for i in range(len(data.quest_names))]
    
    session.add_all(quests)
    session.commit()
    
    
if __name__ == '__main__':
    print('Seeding database')
    seed_db()
    print('Seeding complete')