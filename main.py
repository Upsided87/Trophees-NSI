"""Entrée principale du jeu Robot Farmer (stub).
Lance le moteur de jeu.
"""
import tkinter as tk
from game import moteur 
from game.carte import Carte

def main():
    print("Robot Farmer — démarrage (stub)")
    # TODO: initialiser le moteur du jeu
    root = tk.Tk()
    root.title("Robot Farmer")
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()
    carte = Carte()

    root.mainloop()     

if __name__ == "__main__":
    main()
