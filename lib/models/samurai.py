from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import Session

class Samurai(Base):
    
    __tablename__ = 'samurais'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    rank = Column(String)
    skill_level = Column(Integer)
    bushido = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    clan_id = Column(Integer, ForeignKey('clans.id'))
    
    def __repr__(self):
        return f"<Samurai {self.id}: {self.name}>"
    
    def dual_history(self):
        pass
    
    def completed_quests(self):
        pass
    
    def challenge(self, opponent, wager):
        pass
    
    def repair_weapon(self, weapon):
        pass
    
    