import pygame 
import pytmx
import pyscroll
from player import Player

#======Variables======
LARGEUR, HAUTEUR = 800, 600

#=====================

class Game : 
    def __init__(self):
        # Créer la fenêtre du jeu 
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Terraformers")
        
        # Charger la carte en format .tmx 
        tmx_data = pytmx.load_pygame('map/world.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # Gestion de l'affichage de la carte avec défilement
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2 # Niveau de zoom sur la carte 
        
        # Générer le joueur à partir du point défini dans Tiled
        player_position = tmx_data.get_object_by_name("Player")
        self.player = Player(player_position.x, player_position.y) 
        
        # Initialisation des listes d'objets du monde
        self.walls = []             # Rectangles pour les collisions
        self.all_resources = []      # Sources de ressources (minerais, bois, etc.)
        self.buildings = []         # Bâtiments (extracteurs, panneaux, générateurs)
        
        # Parcours de tous les objets de la carte Tiled pour les trier
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                # Ajout aux murs de collision
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            else:
                # Identification dynamique des ressources par type ou par nom
                is_resource = False
                res_type = 'metal'
                # On concatène type et nom pour une recherche plus flexible (casse insensible)
                target = (obj.type if obj.type else "") + (obj.name if obj.name else "")
                target = target.lower()
                
                # Mappage des mots-clés vers les types de ressources internes
                if 'silicium' in target: res_type, is_resource = 'silicium', True
                elif any(k in target for k in ['metal', 'métal']): res_type, is_resource = 'metal', True
                elif any(k in target for k in ['wood', 'bois', 'arbre']): res_type, is_resource = 'wood', True
                elif any(k in target for k in ['stone', 'pierre', 'roche']): res_type, is_resource = 'stone', True
                
                if is_resource:
                    # Stockage des données de la ressource
                    self.all_resources.append({
                        'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        'type': res_type,
                        'available': True,       # Indique si elle peut être récoltée
                        'harvest_time': 0        # Moment de la dernière récolte (pour regen)
                    })
                # Identification des bâtiments environnementaux
                elif obj.type and ('extract_co2' in obj.type or 'solar_panel' in obj.type or 'generator' in obj.type):
                    self.buildings.append({
                        'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        'repaired': False,       # État initial : cassé
                        'level': 1,              # Niveau initial
                        'type': obj.type,
                        'name': obj.name
                    })
                
        print("Rectangles de collision chargés :", len(self.walls))
        
        # État initial de la dépollution
        self.depollution = 0
        self.depollution_speed = 0.05            # Vitesse de base du nettoyage
        self.last_passive_gen = pygame.time.get_ticks() # Timer pour les revenus des générateurs
        
        self.menu_running = True # Le jeu commence par l'affichage des commandes
        
        # Initialisation du groupe de sprites avec gestion du calque de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)
        
    def handle_input(self):
        """Gère les entrées clavier pour le déplacement continu."""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: self.player.move_up()
        if pressed[pygame.K_DOWN]: self.player.move_down()
        if pressed[pygame.K_LEFT]: self.player.move_left()
        if pressed[pygame.K_RIGHT]: self.player.move_right()
            
    def handle_interaction(self, event):
        """Gère les interactions ponctuelles (récolte, réparation, upgrade)."""
        if event.type == pygame.KEYDOWN:
            # Touche E : RÉCOLTE
            if event.key == pygame.K_e:
                for res in self.all_resources:
                    # On vérifie la proximité et la disponibilité
                    if res['available'] and self.player.rect.colliderect(res['rect']):
                        self.player.resources[res['type']] += 10
                        res['available'] = False
                        res['harvest_time'] = pygame.time.get_ticks()
                        print(f"Récolté 10 {res['type']}. Repousse dans 30s.")
                        break
            
            # Touche R : RÉPARATION
            if event.key == pygame.K_r:
                for bld in self.buildings:
                    if self.player.rect.colliderect(bld['rect']) and not bld['repaired']:
                        # Coût de base 20/10, sauf pour les panneaux solaires (10/5)
                        cost_m, cost_s = 20, 10
                        if 'solar_panel' in bld['type']: cost_m, cost_s = 10, 5
                            
                        if self.player.resources['metal'] >= cost_m and self.player.resources['silicium'] >= cost_s:
                            self.player.resources['metal'] -= cost_m
                            self.player.resources['silicium'] -= cost_s
                            bld['repaired'] = True
                            print(f"{bld['name']} réparé !")
                        else:
                            print(f"Ressources insuffisantes (besoin: {cost_m} Metal, {cost_s} Silicium)")
                        break
            
            # Touche U : AMÉLIORATION (Upgrade)
            if event.key == pygame.K_u:
                for bld in self.buildings:
                    if self.player.rect.colliderect(bld['rect']) and bld['repaired']:
                        if bld['level'] < 3:
                            # Le coût augmente avec le niveau
                            cost_metal = 40 * bld['level']
                            cost_silicium = 20 * bld['level']
                            if self.player.resources['metal'] >= cost_metal and self.player.resources['silicium'] >= cost_silicium:
                                self.player.resources['metal'] -= cost_metal
                                self.player.resources['silicium'] -= cost_silicium
                                bld['level'] += 1
                                print(f"{bld['name']} amélioré au niveau {bld['level']} !")
                            else:
                                print(f"Ressources insuffisantes pour l'amélioration ({cost_metal}M / {cost_silicium}S)")
                        else:
                            print(f"{bld['name']} est au niveau maximum.")
                        break
            
    def update(self):
        """Mise à jour de la logique du jeu à chaque frame."""
        self.group.update()

        # Gestion des collisions avec les murs (on repousse le joueur vers sa position précédente)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1 : 
                sprite.move_back()
                
        # --- Calcul de la dépollution ---
        repaired_buildings = [b for b in self.buildings if b['repaired']]
        # Capacité électrique totale (somme des niveaux des panneaux réparés)
        total_solar_capacity = sum(b['level'] for b in repaired_buildings if 'solar_panel' in b['type'])
        
        # Priorité aux extracteurs de haut niveau pour consommer l'énergie
        repaired_co2 = sorted([b for b in repaired_buildings if 'extract_co2' in b['type']], key=lambda x: x['level'], reverse=True)
        
        active_co2_power = 0
        used_energy = 0
        for co2 in repaired_co2:
            # 1 extracteur Lvl X consomme X points d'énergie
            needed = co2['level']
            if used_energy + needed <= total_solar_capacity:
                used_energy += needed
                # Boost de dépollution basé sur le niveau (0.2 par niveau)
                active_co2_power += 0.2 * co2['level']
            else: break # Plus d'énergie disponible
                
        # Impact passif des autres bâtiments (panneaux, générateurs)
        other_repaired_impact = sum(0.05 * b['level'] for b in repaired_buildings if 'extract_co2' not in b['type'])

        # La dépollution ne tourne QUE si au moins un extracteur est alimenté
        if active_co2_power > 0:
            current_speed = self.depollution_speed + other_repaired_impact + active_co2_power
        else:
            current_speed = 0 # Nettoyage à l'arrêt
        
        if self.depollution < 100:
            self.depollution += current_speed / 60 # Normalisation selon le framerate (60 FPS)
            if self.depollution > 100: self.depollution = 100

        # --- Gestion de la régénération des ressources ---
        current_time = pygame.time.get_ticks()
        for res in self.all_resources:
            if not res['available'] and current_time - res['harvest_time'] > 30000:
                res['available'] = True
                print(f"Régénération : {res['type']} de nouveau disponible.")

        # --- Génération passive des générateurs ---
        if current_time - self.last_passive_gen > 5000: # Toutes les 5s
            repaired_gens = [b for b in repaired_buildings if 'generator' in b['type']]
            if repaired_gens:
                total_metal = sum(2 * b['level'] for b in repaired_gens)
                total_silicium = sum(1 * b['level'] for b in repaired_gens)
                self.player.resources['metal'] += total_metal
                self.player.resources['silicium'] += total_silicium
            self.last_passive_gen = current_time

    def draw_resource_bars(self):
        """Affiche les petites barres d'état (vert/jaune) au-dessus des minerais."""
        view_rect = self.map_layer.view_rect
        zoom = self.map_layer.zoom
        current_time = pygame.time.get_ticks()
        
        for res in self.all_resources:
            # Transformation des coordonnées monde -> écran
            world_x = res['rect'].centerx
            world_y = res['rect'].y - 10 
            screen_x = (world_x - view_rect.x) * zoom
            screen_y = (world_y - view_rect.y) * zoom
            
            if 0 <= screen_x <= LARGEUR and 0 <= screen_y <= HAUTEUR:
                if res['available']:
                    progress, bar_color = 1.0, (0, 255, 0)
                else:
                    elapsed = current_time - res['harvest_time']
                    progress, bar_color = min(elapsed / 30000, 1.0), (255, 255, 0)
                
                bar_width = 32 * zoom
                bar_height = 4 * zoom
                pygame.draw.rect(self.screen, (0, 0, 0), (screen_x - bar_width/2, screen_y, bar_width, bar_height))
                pygame.draw.rect(self.screen, bar_color, (screen_x - bar_width/2, screen_y, int(bar_width * progress), bar_height))

    def draw_building_info(self):
        """Affiche le niveau ou l'avis de réparation au-dessus des bâtiments."""
        view_rect = self.map_layer.view_rect
        zoom = self.map_layer.zoom
        font = pygame.font.SysFont("Arial", 14)
        
        for bld in self.buildings:
            world_x = bld['rect'].centerx
            world_y = bld['rect'].y - 5
            screen_x = (world_x - view_rect.x) * zoom
            screen_y = (world_y - view_rect.y) * zoom
            
            if 0 <= screen_x <= LARGEUR and 0 <= screen_y <= HAUTEUR:
                status_text = f"Niveau {bld['level']}"
                color = (255, 255, 255)
                if not bld['repaired']:
                    status_text, color = "À RÉPARER", (255, 100, 100)
                
                txt_surface = font.render(status_text, True, color)
                txt_rect = txt_surface.get_rect(center=(screen_x, screen_y))
                pygame.draw.rect(self.screen, (0, 0, 0, 180), txt_rect.inflate(4, 2))
                self.screen.blit(txt_surface, txt_rect)

    def draw_ui(self):
        """Affiche l'interface utilisateur (inventaire, barre globale)."""
        # Panneau des ressources
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 100))
        font = pygame.font.SysFont("Arial", 16)
        y_off = 15
        for res_name in ['metal', 'silicium']:
            val = self.player.resources[res_name]
            text = font.render(f"{res_name.capitalize()}: {val}", True, (255, 255, 255))
            self.screen.blit(text, (20, y_off))
            y_off += 20
            
        # Barre de dépollution principale
        pygame.draw.rect(self.screen, (100, 100, 100), (300, 20, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 100), (300, 20, int(self.depollution * 2), 20))
        text_depol = font.render(f"Dépollution: {int(self.depollution)}%", True, (255, 255, 255))
        self.screen.blit(text_depol, (340, 45))

        # Indicateur d'énergie solaire et alerts
        repaired_buildings = [b for b in self.buildings if b['repaired']]
        total_solar = sum(b['level'] for b in repaired_buildings if 'solar_panel' in b['type'])
        total_co2_needs = sum(b['level'] for b in repaired_buildings if 'extract_co2' in b['type'])
        
        energy_color = (100, 255, 100) if total_solar >= total_co2_needs else (255, 100, 100)
        energy_text = font.render(f"Énergie Solaire: {total_solar}/{total_co2_needs}", True, energy_color)
        self.screen.blit(energy_text, (340, 70))
        
        if total_solar < total_co2_needs and any('extract_co2' in b['type'] for b in repaired_buildings):
            warn_text = font.render("Alarm: Énergie insuffisante !", True, (255, 100, 100))
            self.screen.blit(warn_text, (300, 90))
        
        if total_co2_needs == 0:
             no_active = font.render("DÉPOLLUTION À L'ARRÊT (CO2 requis)", True, (255, 50, 50))
             self.screen.blit(no_active, (310, 90))

    def draw_menu(self):
        """Dessine l'overlay du menu des commandes au lancement."""
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) # Noir transparent
        self.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.SysFont("Arial", 36, bold=True)
        font_text = pygame.font.SysFont("Arial", 22)
        
        title = font_title.render("PROTOCOLE TERRAFORMER", True, (0, 255, 100))
        self.screen.blit(title, (LARGEUR//2 - title.get_width()//2, 80))
        
        commands = [
            "ACTIONS DISPONIBLES :",
            "- Flèches : Piloter le drone",
            "- E (sur minerai) : Récolter des matériaux",
            "- R (sur bâtiment) : Réparer avec Métal et Silicium",
            "- U (sur bâtiment réparé) : Améliorer les performances",
            "",
            "OBJECTIFS :",
            "- Collectez du Métal et du Silicium.",
            "- Réparez des Panneaux Solaires pour alimenter les machines.",
            "- Démarrez les Extracteurs de CO2 pour dépolluer l'atmosphère.",
            "",
            "Appuyez sur n'importe quelle touche pour lancer le drone..."
        ]
        
        y = 160
        for line in commands:
            color = (255, 255, 255)
            if "ACTIONS" in line or "OBJECTIFS" in line: color = (100, 200, 255)
            if "lancer" in line: color = (0, 255, 100)
            text = font_text.render(line, True, color)
            self.screen.blit(text, (LARGEUR//2 - text.get_width()//2, y))
            y += 30
    
    def run(self): 
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.last_update = self.start_time
        running = True 

        while running:
            # Gestion des évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False 
                
                # Sortie du menu de démarrage
                if self.menu_running:
                    if event.type == pygame.KEYDOWN: self.menu_running = False
                else: self.handle_interaction(event)
            
            # --- Boucle Menu ---
            if self.menu_running:
                self.group.center(self.player.rect)
                self.group.draw(self.screen)
                self.draw_menu()
                pygame.display.flip()
                clock.tick(60)
                continue

            # --- Boucle Jeu Standard ---
            self.current_time = pygame.time.get_ticks()
            self.player.save_location() # Pour la gestion des collisions (annulation mouvement)
            self.handle_input()
            self.update()
            
            # Animation du sprite du drone
            if self.current_time - self.last_update > 50:
                self.player.change_animation()
                self.last_update = self.current_time

            # Centrage de la caméra sur le joueur
            self.group.center(self.player.rect)
            # Rendu de la carte et des sprites
            self.group.draw(self.screen)
            # Rendu des éléments custom par dessus
            self.draw_resource_bars()
            self.draw_building_info()
            self.draw_ui()
            
            pygame.display.flip()
            clock.tick(60) # Limite à 60 images par seconde
            
        pygame.quit()