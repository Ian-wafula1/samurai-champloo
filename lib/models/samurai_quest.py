from sqlalchemy import Table, Column, ForeignKey, Integer
from .base import Base

samurai_quest = Table(
    'samurai_quest',
    Base.metadata,
    Column('samurai_id', Integer, ForeignKey('samurais.id'), primary_key=True),
    Column('quest_id', Integer, ForeignKey('quests.id'), primary_key=True),
    extend_existing=True
)