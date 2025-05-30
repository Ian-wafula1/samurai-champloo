from models import Samurai, Clan, Weapon, Duel, Quest, session

def clear_db():
    session.query(Samurai).delete()
    session.query(Clan).delete()
    session.query(Weapon).delete()
    session.query(Duel).delete()
    for quest in session.query(Quest).all():
        quest.samurais = []
        
    session.query(Quest).delete()
    
    session.commit()