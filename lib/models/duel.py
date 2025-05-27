from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session
import random

class Duel(Base):
    
    __tablename__ = 'duels'
    
    id = Column(Integer, primary_key=True)
    time_held = Column(DateTime, server_default=func.now())
    location = Column(String())
    bushido_wagered = Column(Integer, default=0)
    challenger_id = Column(Integer, ForeignKey('samurais.id'))
    opponent_id = Column(Integer, ForeignKey('samurais.id'))
    winner_id = Column(Integer, ForeignKey('samurais.id'))
    
    def __repr__(self):
        return f"Duel {self.id}: between samurais {self.challenger_id} and {self.opponent_id}"
    
    @property
    def challenger(self):
        from .samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.challenger_id).first()
    
    @property
    def opponent(self):
        from .samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.opponent_id).first()
    
    @property
    def winner(self):
        from .samurai import Samurai
        return session.query(Samurai).filter(Samurai.id == self.winner_id).first()
    
    @property
    def participants(self):
        return [self.challenger, self.opponent]
    
    @staticmethod
    def handle_duel(chal_id, opp_id, wager, location):
        from .samurai import Samurai
        if chal_id == opp_id:
            raise Exception("One can not duel against himself (in Master oogway voice)")
        challenger = session.query(Samurai).filter(Samurai.id == chal_id).first()
        opponent = session.query(Samurai).filter(Samurai.id == opp_id).first()
        print(f"{challenger.name} has challenged {opponent.name} to a duel!")
        
        if not challenger.weapons:
            raise Exception(f"The challenger, {challenger.name} lacks a weapon to participate in the duel")
        
        if not opponent.weapons:
            raise Exception(f"The opponent, {opponent.name} lacks a weapon to participate in the duel")
        
        
        while True:
            print('Challenger!!! Choose your weapon')
            for weapon in challenger.weapons:
                print(f"Weapon {weapon.id}: {weapon.name} | Damage: {weapon.damage} | Durability: {weapon.durability}")
            challenger_weapon = next((weapon for weapon in challenger.weapons if weapon.id == input('Weapon id: ')), None)
            if challenger_weapon:
                break
            else:
                print('Please pick a weapon owned by the challenger')
        
        while True:
            print('Opponent!!! Choose your weapon')
            for weapon in opponent.weapons:
                print(f"Weapon {weapon.id}: {weapon.name} | Damage: {weapon.damage} | Durability: {weapon.durability}")
            opponent_weapon = next((weapon for weapon in opponent.weapons if weapon.id == input('Weapon id: ')), None)
            if opponent_weapon:
                break
            else:
                print('Please pick a weapon owned by the opponent')
        
        if challenger.bushido < wager or opponent.bushido < wager:
            raise ValueError("One of the samurais lacks enough bushido to duel.")
        
        # Logic for deciding winner
        challenger_score = challenger_weapon.damage + challenger.skill_level + random.randint(0,10)
        opponent_score = opponent_weapon.damage + opponent.skill_level + random.randint(0,10)
        
        winner = challenger if challenger_score > opponent_score else opponent
        loser = opponent if winner == challenger else challenger
        
        challenger_weapon.degrade()
        opponent_weapon.degrade()
        
        winner.bushido += wager
        winner.increase_skill('win')
        loser.bushido -= wager
        loser.increase_skill('loss')
        
        duel = Duel(
            time_held = func.now(),
            location = location,
            bushido_wagered = wager,
            challenger_id = chal_id,
            opponent_id = opp_id,
            winner_id = winner.id
        )
        
        session.add_all([duel, challenger_weapon, opponent_weapon, winner, loser])
        session.commit()
        
        return duel
        
        
        
        