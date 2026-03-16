from dataclasses import dataclass
import pygame
import pytmx
import pyscroll

@dataclass
class Map:
    name: str
    walls: list
    group: pyscroll.PyscrollGroup

class MapManager:

    def __init__(self):
        self.maps = dict()  # "world" -> Map("world", walls, group)
        self.current_map = "world"
