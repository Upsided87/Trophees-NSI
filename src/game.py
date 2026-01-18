import pygame 
import pytmx
import pyscroll
from player import Player

#======Variables======
LARGEUR, HAUTEUR = 800, 600

#=====================

class Game : 
    def __init__(self):
        #Creer la fenetre du jeu 
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Terraformers")
        
        #Charger la carte en format .tmx 
        tmx_data = pytmx.load_pygame('map/world.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2 #Zoom sur la carte 
        
        #Générer un joueur
        player_position = tmx_data.get_object_by_name("Player") #Récupère la position du point Player 'defini dans Tiled 
        self.player = Player(player_position.x, player_position.y) #Fait apparaitre le joueur sur ce point 
        
        #Définir une liste qui stock les rectangles de collision
        self.walls = []
        for objects in tmx_data.objects :
            if objects.type == 'collision':
                self.walls.append(pygame.Rect(objects.x, objects.y, objects.width, objects.height))
        print("Rectangles de collision :", self.walls) #TEST
        
        #Dessiner le groupe de calques 
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)
        
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP]:
            self.player.move_up()
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
        if pressed[pygame.K_f]:
            print("f")
            
    def update(self):
        self.group.update()

        #Verification de la collision 
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 : 
                sprite.move_back()
    
    def run(self): 
        
        clock = pygame.time.Clock()
        
        self.start_time = pygame.time.get_ticks() #Temps initial 
        self.last_update = self.start_time
        #Boucle du jeu 
        running = True 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False 
                    
            self.current_time = pygame.time.get_ticks()  # Temps actuel
            self.player.save_location()
            self.handle_input()
            self.update()
            
            #Met a jour le sprite toute les 200 ms pour faire une animation
            if self.current_time - self.last_update > 50:
                self.player.change_animation()
                self.last_update = self.current_time  # Met à jour le dernier temps

            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)
            
        pygame.quit()