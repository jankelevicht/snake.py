Jeu Snake - README
==================

Description
-----------
Ce projet est une implémentation du jeu classique "Snake" en Python, utilisant la bibliothèque Pygame.
Le jeu propose plusieurs modes (classique, vitesse croissante, versus) et des menus graphiques personnalisés.

Pré-requis
----------
- Python 3.8 ou supérieur (ex. Python 3.13.1)
- Pygame (version 2.6.1 ou compatible)

Installation
------------
1. Installe Python depuis https://www.python.org/downloads/
2. Installe Pygame en ouvrant un terminal et en exécutant :
   
      pip install pygame
   
   (ou, selon ton installation, exécute : python -m pip install pygame)
3. Télécharge ou clone ce projet dans un dossier de ton choix.
4. Assure-toi que les fichiers images suivants se trouvent dans le même dossier que le script principal (snake.py) :
   - classique.jpg  : Fond pour les modes "classique" et "vitesse".
   - versus.jpg     : Fond pour le mode "versus".
   - menu.jpg       : Fond pour les menus (début, pause, fin).
   - (Optionnel) Autres images pour personnaliser la tête du serpent, etc.

Exécution
---------
Pour lancer le jeu, ouvre un terminal dans le dossier du projet et exécute :

      python snake.py

Assure-toi d'utiliser la bonne version de Python installée sur ton système.

Contrôles
---------
- Touches directionnelles : Contrôlent la direction du serpent.
- P : Met en pause ou reprend le jeu.
- Au démarrage, le jeu affiche un message en overlay : 
    "Appuyez sur une direction pour commencer"  
    "Appuyez sur P pour faire pause"
  Le jeu démarre uniquement lorsque le joueur appuie sur une touche directionnelle, ce qui garantit que l'IA 
  ne commence qu'après le premier mouvement du joueur.

Modes de jeu
------------
- Classique : Mode standard où le serpent se déplace et grandit en mangeant des pommes.
- Vitesse Croissante : Le serpent accélère à chaque pomme mangée.
- Versus : Le joueur affronte une IA. L'IA démarre uniquement après le premier mouvement du joueur.

Fonctionnalités
---------------
- Menus personnalisés : 
  - Des fonds personnalisés pour les menus (début, pause, fin) sont utilisés.
  - Les instructions (ex. "Appuyez sur une direction pour commencer") s'affichent en overlay sur le jeu, sans 
    masquer le fond.
- Pause : 
  - Le jeu peut être mis en pause en appuyant sur la touche P, et les instructions de reprise sont affichées en overlay.
- Démarrage différé de l'IA :
  - L'IA commence à jouer uniquement après que le joueur a appuyé sur une touche directionnelle.

Améliorations futures
---------------------
- Ajout de niveaux ou d'obstacles dans le jeu.
- Ajout d'animation quand une pomme est mangée.
- Ajout d'image pour la tête du serpent.
- Intégration de power-ups (bonus ou malus).
- Amélioration de l'IA (par exemple, en utilisant des algorithmes de pathfinding comme A*).
- Ajout d'un mode multijoueur (local ou en ligne).
- Sauvegarde et affichage du meilleur score entre les sessions.

Licence
-------
Ce projet est sous licence MIT (ou une autre licence de ton choix).

Bonne utilisation et amuse-toi bien !
