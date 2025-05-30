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
    
    @property
    def details(self):
        return f"{self.name} | Description: {self.description} | Difficulty : {self.difficulty_rating} | Status: {self.status} | Reward: {self.bushido_reward} | ID: {self.id}"
    
    @classmethod
    def assign_quest(cls, quest_id, samurai_id):
        from .samurai import Samurai
        if not (quest := session.query(Quest).filter(Quest.id == quest_id).first()):
            return f"Quest {quest_id} doesn't exist!"
        if not (samurai := session.query(Samurai).filter(Samurai.id == samurai_id).first()):
            return f"Samurai {samurai_id} doesn't exist!"
        if len(quest.samurais) >= 3:
            return 'A quest can only be undertaken by a maximum of 3 samurais'
        if samurai in quest.samurais:
            return f"Samurai {samurai_id} is already assigned to this quest"
        if quest.status == 'completed':
            return f"Quest {quest_id} is already completed"
        quest.status = 'active'
        
        quest.samurais.append(samurai)
        session.add_all([samurai, quest])
        session.commit()
        return f"Quest {quest_id} assigned to Samurai {samurai_id}"
    
    @classmethod
    def complete_quest(cls, quest_id):
        quest = session.query(Quest).filter(Quest.id == quest_id).first()
        if not quest:
            return f"Quest {quest_id} doesn't exist!"
        if quest.status == 'completed':
            return f"Quest {quest_id} is already completed"
        reward = int(quest.bushido_reward / len(quest.samurais))
        for samurai in quest.samurais:
            samurai.bushido += reward
        quest.status = 'completed'
        session.add_all(quest.samurais)
        session.add(quest)
        session.commit()
        
        return f"Quest {quest.id} completed. Reward: {reward} Bushido points"
    