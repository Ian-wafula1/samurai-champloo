from models import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from models import session

class Duel(Base):
    
    __tablename__ = 'duels'
    
    id = Column(Integer, primary_key=True)
    time_held = Column(DateTime, server_default=func.now())
    location = Column(String())
    bushido_wagered = Column(Integer, default=0)
    challenger_id = Column(Integer, ForeignKey('samurai.id'))
    opponent_id = Column(Integer, ForeignKey('samurai.id'))
    winner_id = Column(Integer, ForeignKey('samurai.id'))
    
    def __repr__(self):
        return f"Duel {self.id}: between samurais {self.challenger_id} and {self.opponent_id}"
    
    @property
    def challenger(self):
        from models.samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.challenger_id).first()
    
    @property
    def opponent(self):
        from models.samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.opponent_id).first()
    
    @property
    def winner(self):
        from models.samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.winner_id).first()
    
    @property
    def participants(self):
        return [self.challenger, self.opponent]
    
    