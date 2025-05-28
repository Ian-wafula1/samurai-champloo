from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session
from .samurai_quest import samurai_quest

class Quest(Base):
    
    __tablename__ = 'quests'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    type = Column(String)
    difficulty_rating = Column(Integer)
    bushido_reward = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, onupdate=func.now())

    samurais = relationship('Samurai', back_populates='quests', secondary=samurai_quest)
    
    def __repr__(self):
        return f"Quest {self.id}: {self.name}"
    
    @classmethod
    def assign_quest(cls, quest_id, samurai_id):
        from .samurai import Samurai
        if not (quest := session.query(Quest).filter(Quest.id == quest_id).first()):
            print(f"Quest {quest_id} doesn't exist!")
            return
        if not (samurai := session.query(Samurai).filter(Samurai.id == quest_id).first()):
            print(f"Samurai {samurai_id} doesn't exist!")
            return
        
        if len(quest.samurais) >= 3:
            print('A quest can only be undertaken by a maximum of 3 samurais')
            return
        
        quest.samurais.append(samurai)
        session.add([samurai, quest])
        session.commit()
        
    
    def complete_quest(self):
        reward = int(self.bushido_reward / self.samurais)
        for samurai in self.samurais:
            samurai.bushido += reward
        session.add_all(self.samurais)
        session.commit()
            

    