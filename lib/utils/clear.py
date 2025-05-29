from models import Samurai, Clan, Weapon, Duel, Quest, session

def clear_db():
    session.query(Samurai).delete()
    session.query(Clan).delete()
    session.query(Weapon).delete()
    session.query(Duel).delete()
    session.query(Quest).delete()
    
    session.commit()