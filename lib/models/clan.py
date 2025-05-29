from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session

class Clan(Base):
    __tablename__ = 'clans'
    __table_args__ = (
        UniqueConstraint('dojo', name='unique_dojo_name'),)
    
    id = Column(Integer,  primary_key=True)
    name = Column(String())
    dojo = Column(String())
    leader_id = Column(String())  
    
    samurais = relationship('Samurai', back_populates='clan')
    
    @property
    def leader(self):
        from .samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.leader_id).first().name
    
    @property
    def details(self):
        return f"Clan Name: {self.name}, Dojo: {self.dojo}, Leader: {self.leader}"
    
    def clan_bushido_total(self):
        from .samurai import Samurai
        return sum([samurai.bushido for samurai in self.samurais])
    
    
    def __repr__(self):
        return f"<Clan {self.id}: {self.name}>"