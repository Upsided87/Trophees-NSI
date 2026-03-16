# Présentation du projet — Terraformers

## Identité du projet

- **Nom du projet** : Terraformers — Mission de Sauvetage Environnemental
- **Niveau** : Terminale NSI
- **Nombre de membres** : 2 élèves
- **Année scolaire** : 2025–2026

---

## Description générale

Terraformers est un jeu vidéo de gestion et d'exploration en vue du dessus, développé entièrement en Python avec la bibliothèque Pygame. Le joueur pilote un drone sur une planète polluée et doit collecter des ressources (Métal, Silicium), réparer des infrastructures (panneaux solaires, générateurs, extracteurs de CO2) et gérer sa consommation énergétique pour atteindre 100% de dépollution atmosphérique.

---

## Problématique traitée

Comment simuler un système de gestion énergétique et environnementale dans un jeu vidéo en 2D, en combinant exploration, collecte de ressources et mécanique de progression ?

---

## Fonctionnalités principales

- Déplacement libre du drone sur une carte générée avec Tiled (.tmx)
- Système de collision basé sur des rectangles chargés depuis la carte
- Récolte de ressources (Métal et Silicium) avec minuterie de régénération de 30 secondes
- Réparation et amélioration de bâtiments (jusqu'au niveau 3) avec coût en ressources
- Gestion de l'énergie solaire : les extracteurs de CO2 consomment de l'énergie produite par les panneaux solaires
- Barre de dépollution progressive (objectif : 100%)
- Génération passive de ressources par les générateurs électriques
- Interface utilisateur affichant l'inventaire, la dépollution et l'état énergétique
- Menu d'introduction avec les commandes du jeu

---

## Architecture technique

Le projet est organisé en plusieurs modules Python :

| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée, initialisation de Pygame et lancement du jeu |
| `game.py` | Classe principale : boucle de jeu, gestion des événements, rendu |
| `player.py` | Classe du joueur (drone) : déplacements, animations, inventaire |
| `map.py` | Structures de données pour la gestion des cartes Tiled |

Les données de la carte sont chargées via **pytmx** et rendues avec **pyscroll**, ce qui permet un défilement fluide et une séparation nette entre les données de jeu et la logique.

---

## Choix techniques justifiés

- **Python / Pygame** : seul langage autorisé au programme NSI, Pygame offre une gestion complète de la fenêtre, des événements et du rendu 2D.
- **Tiled + pytmx** : permet de concevoir la carte visuellement, de définir des zones de collision et de placer des objets nommés directement dans l'éditeur, sans codage en dur.
- **pyscroll** : gestion du défilement de la carte centrée sur le joueur.
- **Sprites en feuille (spritesheet)** : optimisation du chargement graphique et animation par alternance de frames.

---

## Utilisation de l'Intelligence Artificielle

Dans ce projet, nous avons eu recours à des outils d'intelligence artificielle de manière ponctuelle et encadrée :

- **Aide à la structuration du code** : l'IA a été consultée pour suggérer une organisation modulaire du projet (séparation `game.py` / `player.py` / `map.py`).
- **Débogage** : certains messages d'erreur Python ont été soumis à l'IA pour obtenir des pistes de correction.
- **Documentation** : l'IA a aidé à formuler certains commentaires et docstrings en français.

L'ensemble de la logique de jeu, des mécaniques (énergie, dépollution, collisions, régénération), de la conception de la carte et du choix des assets a été réalisé par les membres de l'équipe. Le code final a été relu, compris et validé par les deux élèves.

---

## Pistes d'évolution

- Ajout d'une carte plus grande avec zones distinctes
- Système de sauvegarde de la progression
- Nouvelles ressources et bâtiments (station météo, filtre à particules)
- Effets sonores et musique d'ambiance
- Écran de victoire animé à 100% de dépollution
- Intelligence artificielle pour des drones ennemis (pollution active)
