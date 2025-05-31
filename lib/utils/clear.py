from models import Samurai, Clan, Weapon, Duel, Quest, session
from sqlalchemy import text

def clear_db():
    session.query(Samurai).delete()
    session.query(Clan).delete()
    session.query(Weapon).delete()
    session.query(Duel).delete()
    
    session.execute(text("DELETE FROM samurai_quest"))
        
    session.query(Quest).delete()
    
    session.commit()