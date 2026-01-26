import pygame 

#======Variables======


#=====================

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        # Chargement de la feuille de sprites du drone
        self.sprite_sheet = pygame.image.load('sprites/drone.png')
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 3
        
        # Initialisation de l'inventaire du joueur
        self.resources = {
            'metal': 0,
            'silicium': 0,
            'wood': 0,
            'stone': 0
        }
        
        # Images pour l'animation (simple alternance de frames)
        self.images = {
            'frame1': self.get_image(0, 0),
            'frame2': self.get_image(0, 32),
        }
        self.current_image = 'frame1'
        
        # Rectangle de détection des pieds pour les collisions précises
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 32)
        self.old_position = self.position.copy()
        
    def save_location(self): 
        """Mémorise la position actuelle avant le prochain mouvement."""
        self.old_position = self.position.copy()
        
    def change_animation(self):
        """Alterne l'image du sprite pour créer un effet visuel de vol."""
        self.current_image = 'frame2' if self.current_image == 'frame1' else 'frame1'
        self.image = self.images[self.current_image]

    # --- Méthodes de déplacement ---
    def move_right(self): self.position[0] += self.speed
    
    def move_left(self): self.position[0] -= self.speed
    
    def move_up(self): self.position[1] -= self.speed
    
    def move_down(self): self.position[1] += self.speed
        
    def update(self):
        """Met à jour le rectangle principal et le rectangle des 'pieds' selon la position."""
        self.rect.topleft = self.position 
        self.feet.midbottom = self.rect.midbottom
        
    def move_back(self):
        """Annule le dernier mouvement en cas de collision."""
        self.position = self.old_position
        self.update()
        
    def get_image(self, x, y):
        """Extrait une frame 32x32 de la feuille de sprites."""
        image = pygame.Surface([32, 32], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image 
    
    def set_speed(self, speed): 
        self.speed = speed