#Programme qui gère le joueur(drone) 

class Player: 
    def __init__(self): #TODO: Rajouter autres variables(énergie, ressources, etc...)
        self.x = 0 
        self.y = 0 
    
        def get_position(self): 
            return (self.x, self.y) #Renvoie la position du joueur
        
        def set_position(self, x, y): #TODO: Rajouter des sécurité pour ne pas sortir de la map
            self.x = x 
            self.y = y
        
        def deplacer_x(self): #TODO: Rajouter des sécurité pour ne pas sortir de la map
            # Permet de déplacer le joueur sur l'axe x (abscisse)
            self.x += 1
            
        def deplacer_y(self): #TODO: Rajouter des sécurité pour ne pas sortir de la map
            # Permet de déplacer le joueur sur l'axe y (ordonnée)
            self.y += 1