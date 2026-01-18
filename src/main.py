import os
import pygame 
from game import Game

#======Variables======


#=====================

if __name__ == '__main__':
    pygame.init()
    game = Game()
    os.chdir("..")
    game.run()

