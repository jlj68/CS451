K_FACTOR = 32

class User:
    def __init__(self, name):
        self.username = name
        self.wins = 0
        self.losses = 0
        self.rating = 1400

    def updateRating(self, opponent, outcome):
        r1 = pow(10, self.rating / 400)
        r2 = pow(10, opponent.rating / 400)

        e1 = r1 / (r1 + r2)
        e2 = r2 / (r1 + r2)

        if outcome is "W":
            s1 = 1
            s2 = 0
        elif outcome is "L":
            s1 = 0
            s2 = 1
        elif outcome is "D":
            s1 = 0.5
            s2 = 0.5

        self.rating = r1 + K_FACTOR * (s1 - e1)
        opponent.rating = r2 + K_FACTOR * (s2 - e2)
