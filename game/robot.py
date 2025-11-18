"""Logique et état des robots (stub)."""

class Robot:
    def __init__(self, id, x=0, y=0):
        self.id = id
        self.x = x
        self.y = y
        self.energy = 100

    def __repr__(self):
        return f"<Robot {self.id} ({self.x},{self.y}) E={self.energy}>"
