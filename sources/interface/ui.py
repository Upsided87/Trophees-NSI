import pygame

LARGEUR, HAUTEUR = 800, 600


class UI:
    """Gère tout le rendu de l'interface utilisateur (HUD, menus, infos monde)."""

    def __init__(self, screen):
        self.screen = screen

    # ------------------------------------------------------------------
    # Menu d'introduction
    # ------------------------------------------------------------------

    def draw_menu(self):
        """Dessine l'overlay du menu des commandes au lancement."""
        overlay = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        font_title = pygame.font.SysFont("Arial", 36, bold=True)
        font_text  = pygame.font.SysFont("Arial", 22)

        title = font_title.render("PROTOCOLE TERRAFORMER", True, (0, 255, 100))
        self.screen.blit(title, (LARGEUR // 2 - title.get_width() // 2, 80))

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
            if "ACTIONS" in line or "OBJECTIFS" in line:
                color = (100, 200, 255)
            if "lancer" in line:
                color = (0, 255, 100)
            text = font_text.render(line, True, color)
            self.screen.blit(text, (LARGEUR // 2 - text.get_width() // 2, y))
            y += 30

    # ------------------------------------------------------------------
    # HUD principal
    # ------------------------------------------------------------------

    def draw_ui(self, player, buildings, depollution):
        """Affiche l'inventaire, la barre de dépollution et l'état énergétique."""
        font = pygame.font.SysFont("Arial", 16)

        # Panneau ressources
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, 200, 100))
        y_off = 15
        for res_name in ['metal', 'silicium']:
            val  = player.resources[res_name]
            text = font.render(f"{res_name.capitalize()}: {val}", True, (255, 255, 255))
            self.screen.blit(text, (20, y_off))
            y_off += 20

        # Barre de dépollution
        pygame.draw.rect(self.screen, (100, 100, 100), (300, 20, 200, 20))
        pygame.draw.rect(self.screen, (0, 255, 100),   (300, 20, int(depollution * 2), 20))
        text_depol = font.render(f"Dépollution: {int(depollution)}%", True, (255, 255, 255))
        self.screen.blit(text_depol, (340, 45))

        # Indicateur énergie solaire
        repaired = [b for b in buildings if b['repaired']]
        total_solar    = sum(b['level'] for b in repaired if 'solar_panel'  in b['type'])
        total_co2_needs= sum(b['level'] for b in repaired if 'extract_co2' in b['type'])

        energy_color = (100, 255, 100) if total_solar >= total_co2_needs else (255, 100, 100)
        energy_text  = font.render(f"Énergie Solaire: {total_solar}/{total_co2_needs}", True, energy_color)
        self.screen.blit(energy_text, (340, 70))

        if total_solar < total_co2_needs and any('extract_co2' in b['type'] for b in repaired):
            warn = font.render("Alarm: Énergie insuffisante !", True, (255, 100, 100))
            self.screen.blit(warn, (300, 90))

        if total_co2_needs == 0:
            no_active = font.render("DÉPOLLUTION À L'ARRÊT (CO2 requis)", True, (255, 50, 50))
            self.screen.blit(no_active, (310, 90))

    # ------------------------------------------------------------------
    # Infos monde (ressources + bâtiments)
    # ------------------------------------------------------------------

    def draw_resource_bars(self, all_resources, map_layer):
        """Affiche les barres de régénération des gisements."""
        current_time = pygame.time.get_ticks()
        view_rect    = map_layer.view_rect
        zoom         = map_layer.zoom

        for res in all_resources:
            world_x  = res['rect'].centerx
            world_y  = res['rect'].y - 10
            screen_x = (world_x - view_rect.x) * zoom
            screen_y = (world_y - view_rect.y) * zoom

            if 0 <= screen_x <= LARGEUR and 0 <= screen_y <= HAUTEUR:
                if res['available']:
                    progress, bar_color = 1.0, (0, 255, 0)
                else:
                    elapsed   = current_time - res['harvest_time']
                    progress  = min(elapsed / 30000, 1.0)
                    bar_color = (255, 255, 0)

                bar_w = 32 * zoom
                bar_h = 4  * zoom
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (screen_x - bar_w / 2, screen_y, bar_w, bar_h))
                pygame.draw.rect(self.screen, bar_color,
                                 (screen_x - bar_w / 2, screen_y, int(bar_w * progress), bar_h))

    def draw_building_info(self, buildings, map_layer):
        """Affiche le niveau ou l'avis de réparation au-dessus des bâtiments."""
        view_rect = map_layer.view_rect
        zoom      = map_layer.zoom
        font      = pygame.font.SysFont("Arial", 14)

        for bld in buildings:
            world_x  = bld['rect'].centerx
            world_y  = bld['rect'].y - 5
            screen_x = (world_x - view_rect.x) * zoom
            screen_y = (world_y - view_rect.y) * zoom

            if 0 <= screen_x <= LARGEUR and 0 <= screen_y <= HAUTEUR:
                if bld['repaired']:
                    status_text = f"Niveau {bld['level']}"
                    color       = (255, 255, 255)
                else:
                    status_text = "À RÉPARER"
                    color       = (255, 100, 100)

                txt_surface = font.render(status_text, True, color)
                txt_rect    = txt_surface.get_rect(center=(screen_x, screen_y))
                pygame.draw.rect(self.screen, (0, 0, 0, 180), txt_rect.inflate(4, 2))
                self.screen.blit(txt_surface, txt_rect)
