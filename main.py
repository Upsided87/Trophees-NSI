import pygame
from sources.jeu.game import Game

if __name__ == '__main__':
    # Initialisation globale de Pygame (vidéo, son, événements)
    pygame.init()
    try:
        # Création de l'instance principale du jeu
        game = Game()
        # Lancement de la boucle principale
        game.run()
    except Exception as e:
        print(f"Erreur lors du lancement du jeu : {e}")
        import traceback
        traceback.print_exc()
