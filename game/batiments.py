"""Définition des bâtiments et leurs interactions (stub)."""

class Batiment:
    def __init__(self, type_name, x, y):
        self.type = type_name
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Batiment {self.type} ({self.x},{self.y})>"
