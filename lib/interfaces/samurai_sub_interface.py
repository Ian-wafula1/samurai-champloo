from models import Duel, Samurai, session

class SamuraiSubInterface:
    
    @staticmethod
    def menu():
        print("0. Exit program \
            1. View details \
            2. Start duel \
            3. View owned weapons \
            4. Buy Weapon \
            5. Sell Weapon \
            6. Join clan \
            7. Leave current clan \
            8. Participate in quest ")
        
    @staticmethod
    def run(id):
        pass