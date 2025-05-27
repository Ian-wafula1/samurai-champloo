from models import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from models import session

class Weapon(Base):
    
    __tablename__ = 'weapons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    damage = Column(Integer)
    durability = Column(Integer, default=100)
    bushido_cost = Column(Integer)
    samurai_id = Column(Integer, ForeignKey('samurais.id'))
    
    @classmethod
    def break_weapon(cls, weapon_id):
        pass
    
    def degrade(self):
        pass
        
    def repair(self):
        self.durability = 100
        