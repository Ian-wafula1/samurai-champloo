from models import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from models import session

class Clan(Base):
    __tablename__ = 'clans'
    __table_args__ = (
        UniqueConstraint('dojo', name='unique_dojo_name'),
        UniqueConstraint('leader_id', name='unique_leader_id')
    )
    
    id = Column(Integer,  primary_key=True)
    name = Column(String())
    dojo = Column(String())
    leader_id = Column(Integer(), ForeignKey('samurais.id'))
    
    @property
    def leader(self):
        from models.samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.leader_id).first().name
    
    @property
    def details(self):
        return f"Clan Name: {self.name}, Dojo: {self.dojo}, Leader: {self.leader}"
    
    @property
    def members(self):
        from models.samurai import Samurai
        return session.query(Samurai).filter(Samurai.clan_id == self.id).all()
    
    def add_member(self, samurai):
        pass
    
    def remove_member(self, samurai):
        pass
    
    def clan_bushido_total(self):
        pass
    
    
    def __repr__(self):
        return f"<Clan {self.id}: {self.name}>"