"""Gestion de la carte (placeholder).
Contient les structures de données de la map.
"""
class Carte:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[None for _ in range(width)] for _ in range(height)]

    def __repr__(self):
        return f"<Carte {self.width}x{self.height}>"
