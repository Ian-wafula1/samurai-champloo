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
    
    @property
    def details(self):
        return f"Duel {self.id} | Time Held: {self.time_held} | Location: {self.location} | Bushido Wagered: {self.bushido_wagered} | Winner: {self.winner.name}"
    
    def handle_duel(self):
        
        from .samurai import Samurai
        challenger = session.query(Samurai).filter(Samurai.id == self.challenger_id).first()
        opponent = session.query(Samurai).filter(Samurai.id == self.opponent_id).first()
        
        print(f"{challenger.name} has challenged {opponent.name} to a duel!")
        
        if not challenger.weapons:
            print(f"The challenger, {challenger.name} lacks a weapon to participate in the duel")
            return
        
        if not opponent.weapons:
            print(f"The opponent, {opponent.name} lacks a weapon to participate in the duel")
            return
        
        while True:
            print('Challenger!!! Choose your weapon')
            for weapon in challenger.weapons:
                print(f"ID {weapon.id}: {weapon.name} | Damage: {weapon.damage} | Durability: {weapon.durability}")
            challenger_weapon = next((weapon for weapon in challenger.weapons if weapon.id == int(input('Weapon id: '))), None)
            
            if challenger_weapon:
                break
            else:
                print('Please pick a weapon owned by the challenger')
        
        while True:
            print('Opponent!!! Choose your weapon')
            for weapon in opponent.weapons:
                print(f"ID {weapon.id}: {weapon.name} | Damage: {weapon.damage} | Durability: {weapon.durability}")
            opponent_weapon = next((weapon for weapon in opponent.weapons if weapon.id == int(input('Weapon id: '))), None)
            
            if opponent_weapon:
                break
            else:
                print('Please pick a weapon owned by the opponent')
        
        if challenger.bushido < self.bushido_wagered or opponent.bushido < self.bushido_wagered:
            print("One of the samurais lacks enough bushido to duel.")
            return
        
        # Logic for deciding winner
        challenger_score = int(challenger_weapon.damage * 0.6) + challenger.skill_level + random.randint(0,10)
        opponent_score = int(opponent_weapon.damage * 0.6) + opponent.skill_level + random.randint(0,10)
        
        winner = challenger if challenger_score > opponent_score else opponent
        loser = opponent if winner == challenger else challenger
        
        challenger_weapon.degrade()
        opponent_weapon.degrade()
        
        winner.bushido += self.bushido_wagered
        winner.increase_skill('win')
        loser.bushido -= self.bushido_wagered
        loser.increase_skill('loss')
        
        self.winner_id = winner.id
        
        print(f"{winner.name} has won the duel!")
        print(f"{winner.name} has gained {self.bushido_wagered} bushido points and now has {winner.bushido} bushido points")
        print(f"{loser.name} has lost {self.bushido_wagered} bushido points and now has {loser.bushido} bushido points")
        
        session.add(self)
        session.add_all([ challenger_weapon, opponent_weapon, winner, loser])
        session.commit()
        
        return self
        