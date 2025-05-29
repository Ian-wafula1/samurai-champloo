from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session

class Weapon(Base):
    
    __tablename__ = 'weapons'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    damage = Column(Integer)
    durability = Column(Integer, default=100)
    bushido_cost = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    samurai_id = Column(Integer, ForeignKey('samurais.id'), nullable=True)
    
    samurai = relationship('Samurai', back_populates='weapons')
    
    def break_weapon(self):
        session.query(Weapon).filter(Weapon.id == self.id).first().delete()
        session.commit()
        return f"Weapon {self.id} has broken."
    
    def degrade(self):
        self.durability -= 10
        if self.durability <= 0:
            return(self.break_weapon())
        else:
            session.add(self)
            session.commit()
        
    def repair(self):
        self.durability = 100
        return f"Weapon successfully repaired!"
    
    @property
    def details(self):
        return f"{self.name} | Type: {self.type} | Damage: {self.damage} | Cost: {self.bushido_cost}"
        