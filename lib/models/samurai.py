from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session
from .samurai_quest import samurai_quest

class Samurai(Base):
    
    __tablename__ = 'samurais'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    skill_level = Column(Integer)
    bushido = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    clan_id = Column(Integer, ForeignKey('clans.id'))
    
    quests = relationship('Quest', back_populates='samurais', secondary=samurai_quest)
    weapons = relationship('Weapon', back_populates='samurai')
    clan = relationship('Clan', back_populates='samurais')
    
    def __repr__(self):
        return f"<Samurai {self.id}: {self.name}>"
    
    @property
    def weapons(self):
        pass
    
    @property
    def rank(self):
        pass
    
    def purchase_weapon(self):
        pass
    
    def sell_weapon(self):
        pass
    
    def dual_history(self):
        pass
    
    def completed_quests(self):
        pass
    
    def challenge(self, opponent, wager):
        pass
    
    def repair_weapon(self, weapon):
        pass
    
    
    
    