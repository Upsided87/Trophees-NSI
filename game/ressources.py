"""Ressources trouvables sur la carte (stub)."""

class Ressource:
    def __init__(self, type_name, amount):
        self.type = type_name
        self.amount = amount

    def __repr__(self):
        return f"<Ressource {self.type} x{self.amount}>"
