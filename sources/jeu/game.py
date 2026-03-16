import os
import pygame
import pytmx
import pyscroll
from sources.systemes.player import Player
from sources.interface.ui import UI

# ======Variables======
LARGEUR, HAUTEUR = 800, 600
# =====================


class Game:
    def __init__(self):
        # Fenêtre
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Terraformers")

        # Chemin absolu vers la racine du projet
        self.base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        map_path = os.path.join(self.base_dir, 'data', 'map', 'world.tmx')

        # Chargement de la carte Tiled
        tmx_data  = pytmx.load_pygame(map_path)
        map_data  = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size()
        )
        self.map_layer.zoom = 2

        # Joueur
        player_position = tmx_data.get_object_by_name("Player")
        self.player = Player(player_position.x, player_position.y)

        # Listes d'objets du monde
        self.walls         = []
        self.all_resources = []
        self.buildings     = []

        # Tri des objets Tiled
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            else:
                is_resource = False
                res_type    = 'metal'
                target = ((obj.type or "") + (obj.name or "")).lower()

                if 'silicium' in target:
                    res_type, is_resource = 'silicium', True
                elif any(k in target for k in ['metal', 'métal']):
                    res_type, is_resource = 'metal', True
                elif any(k in target for k in ['wood', 'bois', 'arbre']):
                    res_type, is_resource = 'wood', True
                elif any(k in target for k in ['stone', 'pierre', 'roche']):
                    res_type, is_resource = 'stone', True

                if is_resource:
                    self.all_resources.append({
                        'rect':         pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        'type':         res_type,
                        'available':    True,
                        'harvest_time': 0
                    })
                elif obj.type and any(k in obj.type for k in
                                      ['extract_co2', 'solar_panel', 'generator']):
                    self.buildings.append({
                        'rect':     pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                        'repaired': False,
                        'level':    1,
                        'type':     obj.type,
                        'name':     obj.name
                    })

        print("Rectangles de collision chargés :", len(self.walls))

        # État global
        self.depollution         = 0
        self.depollution_speed   = 0.05
        self.last_passive_gen    = pygame.time.get_ticks()
        self.menu_running        = True

        # Groupe de sprites pyscroll
        self.group = pyscroll.PyscrollGroup(
            map_layer=self.map_layer, default_layer=4
        )
        self.group.add(self.player)

        # Interface utilisateur
        self.ui = UI(self.screen)

    # ------------------------------------------------------------------
    # Entrées
    # ------------------------------------------------------------------

    def handle_input(self):
        """Gère les entrées clavier pour le déplacement continu."""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:    self.player.move_up()
        if pressed[pygame.K_DOWN]:  self.player.move_down()
        if pressed[pygame.K_LEFT]:  self.player.move_left()
        if pressed[pygame.K_RIGHT]: self.player.move_right()

    def handle_interaction(self, event):
        """Gère les interactions ponctuelles (récolte, réparation, upgrade)."""
        if event.type != pygame.KEYDOWN:
            return

        # E : Récolte
        if event.key == pygame.K_e:
            for res in self.all_resources:
                if res['available'] and self.player.rect.colliderect(res['rect']):
                    self.player.resources[res['type']] += 10
                    res['available']    = False
                    res['harvest_time'] = pygame.time.get_ticks()
                    print(f"Récolté 10 {res['type']}. Repousse dans 30s.")
                    break

        # R : Réparation
        if event.key == pygame.K_r:
            for bld in self.buildings:
                if self.player.rect.colliderect(bld['rect']) and not bld['repaired']:
                    cost_m, cost_s = (10, 5) if 'solar_panel' in bld['type'] else (20, 10)
                    if (self.player.resources['metal']    >= cost_m and
                            self.player.resources['silicium'] >= cost_s):
                        self.player.resources['metal']    -= cost_m
                        self.player.resources['silicium'] -= cost_s
                        bld['repaired'] = True
                        print(f"{bld['name']} réparé !")
                    else:
                        print(f"Ressources insuffisantes (besoin: {cost_m} Metal, {cost_s} Silicium)")
                    break

        # U : Amélioration
        if event.key == pygame.K_u:
            for bld in self.buildings:
                if self.player.rect.colliderect(bld['rect']) and bld['repaired']:
                    if bld['level'] < 3:
                        cost_m = 40 * bld['level']
                        cost_s = 20 * bld['level']
                        if (self.player.resources['metal']    >= cost_m and
                                self.player.resources['silicium'] >= cost_s):
                            self.player.resources['metal']    -= cost_m
                            self.player.resources['silicium'] -= cost_s
                            bld['level'] += 1
                            print(f"{bld['name']} amélioré au niveau {bld['level']} !")
                        else:
                            print(f"Ressources insuffisantes ({cost_m}M / {cost_s}S)")
                    else:
                        print(f"{bld['name']} est au niveau maximum.")
                    break

    # ------------------------------------------------------------------
    # Mise à jour logique
    # ------------------------------------------------------------------

    def update(self):
        """Mise à jour de la logique du jeu à chaque frame."""
        self.group.update()

        # Collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

        # Dépollution
        repaired       = [b for b in self.buildings if b['repaired']]
        total_solar    = sum(b['level'] for b in repaired if 'solar_panel' in b['type'])
        repaired_co2   = sorted(
            [b for b in repaired if 'extract_co2' in b['type']],
            key=lambda x: x['level'], reverse=True
        )

        active_co2_power = 0
        used_energy      = 0
        for co2 in repaired_co2:
            if used_energy + co2['level'] <= total_solar:
                used_energy      += co2['level']
                active_co2_power += co2['level']

        if active_co2_power > 0 and self.depollution < 100:
            self.depollution = min(
                100,
                self.depollution + self.depollution_speed * active_co2_power
            )

        # Régénération des ressources (30 s)
        current_time = pygame.time.get_ticks()
        for res in self.all_resources:
            if not res['available'] and current_time - res['harvest_time'] >= 30000:
                res['available'] = True

        # Génération passive des générateurs (5 s)
        if current_time - self.last_passive_gen >= 5000:
            for bld in repaired:
                if 'generator' in bld['type']:
                    self.player.resources['metal']    += bld['level']
                    self.player.resources['silicium'] += bld['level']
            self.last_passive_gen = current_time

    # ------------------------------------------------------------------
    # Boucle principale
    # ------------------------------------------------------------------

    def run(self):
        clock            = pygame.time.Clock()
        self.start_time  = pygame.time.get_ticks()
        self.last_update = self.start_time
        running          = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.menu_running:
                    if event.type == pygame.KEYDOWN:
                        self.menu_running = False
                else:
                    self.handle_interaction(event)

            # --- Menu d'introduction ---
            if self.menu_running:
                self.group.center(self.player.rect)
                self.group.draw(self.screen)
                self.ui.draw_menu()
                pygame.display.flip()
                clock.tick(60)
                continue

            # --- Boucle de jeu ---
            self.current_time = pygame.time.get_ticks()
            self.player.save_location()
            self.handle_input()
            self.update()

            # Animation du drone
            if self.current_time - self.last_update > 50:
                self.player.change_animation()
                self.last_update = self.current_time

            # Rendu
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            self.ui.draw_resource_bars(self.all_resources, self.map_layer)
            self.ui.draw_building_info(self.buildings, self.map_layer)
            self.ui.draw_ui(self.player, self.buildings, self.depollution)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
