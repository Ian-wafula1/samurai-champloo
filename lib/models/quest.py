from models import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from models import session

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

    
    def __repr__(self):
        return f"Quest {self.id}: {self.name}"
    
    def participants(self):
        pass
    
    def give_reward(self):
        pass
    
    def check_status(self):
        pass
    