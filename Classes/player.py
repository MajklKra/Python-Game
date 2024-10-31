

class Player:

    def __init__(self, name, position):
        self.name = name           # Proměnná instance
        self.position = 1          # Proměnná instance


    def p_change(self, np):
        self.position = np

    def roll_dice(self):
        import random
        return random.randint(1, 6)