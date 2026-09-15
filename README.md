# Escape-Game-Engine-Pygame

Moteur logique et interface graphique développés en Python pour simuler les interactions d'une salle d'Escape Game. 

Ce projet a été conçu pour valider une architecture logicielle Orientée Objet (POO) avant son intégration dans des systèmes embarqués physiques (microcontrôleurs, capteurs). 

## 🛠️ Architecture Technique

Le code est structuré autour de plusieurs classes distinctes pour séparer la logique métier de l'interface :
*   `joueur.py` : Gestion de l'inventaire et des interactions.
*   `meuble.py` / `objet.py` : Entités interactives avec gestion des états (verrouillé, ouvert, combinable).
*   `salle.py` : Gestion des environnements et des transitions.
*   `interface_pygame.py` : Rendu visuel et boucle d'événements.

La conception permet la création de puzzles complexes (combinaison d'objets, codes d'accès, conditions préalables) détaillés dans le fichier `Solution.txt`.

## 🎮 Tester le projet (Version Compilée)

Une version exécutable (.exe) autonome est disponible pour tester la logique du jeu sans avoir besoin d'installer Python.

👉 **[Accéder à la page de téléchargement de l'exécutable (.exe)](https://github.com/pcurty/Escape-Game-Engine-Pygame/releases/tag/v1.0)**
