from .base import Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime
from .base import session
from .samurai_quest import samurai_quest

class Samurai(Base):
    
    __tablename__ = 'samurais'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    skill_level = Column(Integer, default=10)
    bushido = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    clan_id = Column(Integer, ForeignKey('clans.id'), nullable=True)
    
    quests = relationship('Quest', back_populates='samurais', secondary=samurai_quest)
    weapons = relationship('Weapon', back_populates='samurai')
    clan = relationship('Clan', back_populates='samurais')
    
    def __repr__(self):
        return f"<Samurai {self.id}: {self.name} | {self.rank}>"
    
    def increase_skill(self, result):
        self.skill_level += 7 if result == 'win' else 3
        
    @property
    def details(self):
        return f"{self.name} | Skill: {self.skill_level} | Bushido: {self.bushido} | Rank: {self.rank} | Clan: {self.clan.name if self.clan else 'None'} | ID: {self.id}"
        
    @property
    def rank(self):
        if self.skill_level < 20:
            return "Ashigaru"
        elif self.skill_level < 40:
            return "Ronin"
        elif self.skill_level < 60:
            return "Hatamoto"
        elif self.skill_level < 80:
            return "Samurai"
        elif self.skill_level < 95:
            return "Sensei"
        else:
            return "Shogun"
    
    def purchase_weapon(self, weapon_id):
        from .weapon import Weapon
        if weapon := session.query(Weapon).filter(Weapon.id == weapon_id).first():
            if id := weapon.samurai_id:
                return f"Weapon is already owned by samurai {id}"
            else:
                if self.bushido < weapon.bushido_cost:
                    return "You don't have enough bushido to purchase the weapon. \
                        Engage in duels or participate in quests to earn bushido."
                else:
                    self.bushido -= weapon.bushido_cost
                    weapon.samurai_id = self.id
                    session.commit()
                    return f"Weapon {weapon_id} purchased successfully. You have {self.bushido} bushido left."
        else:
            return f"Weapon {weapon_id} doesn't exist "
    
    def sell_weapon(self, weapon_id):
        from .weapon import Weapon
        weapon = session.query(Weapon).filter(Weapon.id == weapon_id).first()
        if weapon not in self.weapons:
            return f"Weapon {weapon_id} is not in your possession"
        else:
            self.bushido += weapon.bushido_cost
            weapon.samurai_id = None
            session.commit()
            return f"Weapon {weapon_id} successfully sold for {weapon.bushido_cost} bushido! You have {self.bushido}."
            
    @property
    def duels(self):
        from .duel import Duel
        duels = []
        duels.extend(session.query(Duel).filter(Duel.opponent_id == self.id).all())
        duels.extend(session.query(Duel).filter(Duel.challenger_id == self.id).all())
        return duels
    
    @property
    def wins(self):
        return [duel for duel in self.duels if duel.winner_id == self.id]
    
    @property
    def losses(self):
        return [duel for duel in self.duels if duel.winner_id != self.id]
    
    def repair_weapon(self, weapon_id):
        from .weapon import Weapon
        weapon = session.query(Weapon).filter(Weapon.id == weapon_id).first()
        if weapon not in self.weapons:
            return f"Weapon {weapon_id} is not in your possession"
        else:
            cost = int(0.4 * weapon.bushido_cost)
            if self.bushido < cost:
                return "You don't have enough bushido to repair the weapon. \
                        Participate in quests to earn bushido."
            else:
                weapon.repair()
                self.bushido -= cost
                session.commit()
                return f"Weapon {weapon_id} repaired!! You have {self.bushido} bushido left."
            
    def leave_clan(self):
        if clan := self.clan:
            self.clan_id = None
            return f"You have left the clan {clan.name}"
        return "You are not in a clan"
        
    def join_clan(self, clan_id):
        from .clan import Clan
        clan = session.query(Clan).filter(Clan.id == clan_id).first()
        if not clan:
            return f"Clan {clan_id} does not exist"
        else:
            self.clan_id = clan_id
            return f"You have joined the clan {clan.name}"
    