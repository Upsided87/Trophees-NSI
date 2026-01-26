# 🌍 Terraformers - Mission de Sauvetage Environnemental

**Terraformers** est un jeu de gestion et d'exploration développé avec **Pygame**. Pilotez un drone sur une planète polluée, récoltez des ressources et réparez des installations technologiques pour restaurer l'atmosphère.

## 🚀 Installation & Lancement

### Prérequis
Assurez-vous d'avoir Python installé sur votre système.

### Installation des bibliothèques
Ouvrez un terminal dans le dossier du projet et exécutez les commandes suivantes :
```bash
pip install pygame
pip install pytmx
pip install pyscroll
```

### Lancement du jeu
Pour démarrer la mission :
```bash
python src/main.py
```

## 🎮 Commandes du Jeu

| Touche | Action |
| :--- | :--- |
| **Flèches Directionnelles** | Déplacer le drone dans le monde |
| **E** | Récolter un gisement de ressource (Métal, Silicium, etc.) |
| **R** | Réparer un bâtiment endommagé (nécessite des ressources) |
| **U** | Améliorer un bâtiment réparé (jusqu'au niveau 3) |
| **Fermeture fenêtre** | Quitter le jeu |

## ⚙️ Mécaniques de Gameplay

### 💎 Gestion des Ressources
- **Récolte** : Trouvez des minerais sur la carte. Une fois récoltés, ils mettent **30 secondes** à réapparaître. Une barre de progression vous indique le temps restant.
- **Inventaire** : Suivez votre stock de Métal et de Silicium dans l'interface en haut à gauche.

### 🏗️ Infrastructures
- **Panneaux Solaires** : Fournissent l'énergie nécessaire aux machines. Plus leur niveau est élevé, plus ils produisent d'énergie (Lvl 1 = 1 Énergie, Lvl 3 = 3 Énergie).
- **Générateurs Électriques** : Produisent passivement du Métal et du Silicium toutes les 5 secondes une fois réparés.
- **Extracteurs de CO2** : Les outils les plus puissants pour la dépollution. **Attention** : Chaque extracteur consomme de l'énergie solaire selon son niveau. S'il n'y a pas assez d'énergie, l'extracteur s'arrête.

### ☁️ Dépollution
Votre objectif final est d'atteindre **100% de dépollution**. La jauge ne progresse que si au moins un **Extracteur de CO2** est actif et alimenté.

## 🛠️ Développement & Crédits

Ce projet utilise :
- **Tiled** : Pour la conception des cartes ([Télécharger Tiled](https://thorbjorn.itch.io/tiled?download)).
- **Textures** : Pack [Sci-Fi RTS par Kenney](https://kenney.nl/assets/sci-fi-rts).
- **Drone Sprite** : Design vectoriel issu de [Freepik](https://www.freepik.com/free-vector/modern-variety-flat-drones_1348551.htm).
- **Bibliothèques Python** : `pygame`, `pytmx`, `pyscroll`.

---
*Réalisé pour les Trophées NSI.*
