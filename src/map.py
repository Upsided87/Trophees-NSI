from dataclasses import dataclass
import pygame
import pytmx
import pyscroll

@dataclass
class Map:
    name: str 
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    
class MapManager:
    
    def __init__(self):
        self.maps = dict() # "Batiment" -> Map("Batiment", walls, group)
        self.current_map = "world"
        
