from models import session, Duel

class DuelInterface:
    
    @staticmethod
    def menu():
        print("0. Exit the program \
            1. ", end='\n\n')