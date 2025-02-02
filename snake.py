import sys
import random
import pygame

# --- CONSTANTES ---
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 700

# Zone de jeu (zone délimitée par un rectangle)
ZONE_JEU_X = 100
ZONE_JEU_Y = 100
LARGEUR_ZONE_JEU = 600
HAUTEUR_ZONE_JEU = 500

TAILLE_BLOC = 10
FPS_AFFICHAGE = 60         # Taux de rafraîchissement pour l'affichage

# Vitesse initiale (en "déplacements" par seconde)
VITESSE_DEFAUT = 10

# Couleurs
COULEUR_FOND = (0, 0, 0)
COULEUR_BORDURE = (255, 255, 255)
COULEUR_POMME = (255, 0, 0)
COULEUR_SCORE = (255, 255, 255)
# Couleurs de base pour le serpent selon le mode
COULEUR_CLASSIQUE = (0, 255, 0)
COULEUR_VITESSE = (0, 0, 255)
COULEUR_VERSUS = (255, 0, 0)
COULEUR_IA = (255, 255, 0)
COULEUR_BLEU_CIEL = (135, 206, 235)

# --- INITIALISATION DE PYGAME ET CHARGEMENT DES IMAGES ---
pygame.init()
# Création de la fenêtre principale
screen = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Charger les images de fond pour les thèmes de jeu
# Pour les modes "classique" et "vitesse", on utilisera la même image de fond.
IMAGE_FOND_CLASSIQUE = pygame.image.load("classique.jpg").convert()
IMAGE_FOND_VERSUS = pygame.image.load("versus.jpg").convert()

IMAGE_FOND_CLASSIQUE = pygame.transform.scale(IMAGE_FOND_CLASSIQUE, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
IMAGE_FOND_VERSUS = pygame.transform.scale(IMAGE_FOND_VERSUS, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Charger l'image de fond pour les menus (début, pause, fin)
MENU_IMAGE = pygame.image.load("menu.jpg").convert()
MENU_IMAGE = pygame.transform.scale(MENU_IMAGE, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

# Dictionnaire associant chaque mode à son image de fond pour le jeu
FONDS = {
    "classique": IMAGE_FOND_CLASSIQUE,
    "vitesse": IMAGE_FOND_CLASSIQUE,  # Même image pour classique et vitesse
    "versus": IMAGE_FOND_VERSUS
}

# --- CLASSES DU JEU ---

class Snake:
    """ Classe représentant le serpent du joueur. """
    def __init__(self, couleur, debut_x, debut_y):
        self.couleur = couleur
        self.taille_bloc = TAILLE_BLOC
        self.positions = [(debut_x, debut_y)]
        self.direction = (0, 0)  # Pas de mouvement initial
        self.longueur = 1

    def set_direction(self, nouvelle_direction):
        # Empêcher de faire demi-tour
        if (self.direction[0] == -nouvelle_direction[0] and
            self.direction[1] == -nouvelle_direction[1]):
            return
        self.direction = nouvelle_direction

    def deplacer(self):
        tete_x, tete_y = self.positions[-1]
        dx, dy = self.direction
        nouvelle_tete = (tete_x + dx, tete_y + dy)
        self.positions.append(nouvelle_tete)
        if len(self.positions) > self.longueur:
            self.positions.pop(0)

    def grandir(self):
        self.longueur += 1

    def se_mord(self):
        tete = self.positions[-1]
        return tete in self.positions[:-1]

    def afficher(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.couleur,
                             (pos[0], pos[1], self.taille_bloc, self.taille_bloc))


class AISnake:
    """ Classe représentant le serpent IA (mode versus). """
    def __init__(self, couleur, debut_x, debut_y):
        self.couleur = couleur
        self.taille_bloc = TAILLE_BLOC
        self.positions = [(debut_x, debut_y)]
        self.direction = (0, 0)
        self.longueur = 1
        self.vitesse_ia = VITESSE_DEFAUT  # Vitesse de l'IA (déplacements par seconde)

    def deplacer(self):
        tete_x, tete_y = self.positions[-1]
        dx, dy = self.direction
        nouvelle_tete = (tete_x + dx, tete_y + dy)
        self.positions.append(nouvelle_tete)
        if len(self.positions) > self.longueur:
            self.positions.pop(0)

    def grandir(self):
        self.longueur += 1

    def afficher(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.couleur,
                             (pos[0], pos[1], self.taille_bloc, self.taille_bloc))

    def deplacement_ia(self, pomme_x, pomme_y):
        """
        Choisit un mouvement valide qui rapproche le serpent IA de la pomme.
        Retourne "bloque" si aucun mouvement n'est possible,
        True si le mouvement est effectué (et éventuellement la pomme a été mangée),
        ou False si le mouvement est effectué sans manger la pomme.
        """
        mouvements_possibles = [
            (TAILLE_BLOC, 0),    # Droite
            (-TAILLE_BLOC, 0),   # Gauche
            (0, TAILLE_BLOC),    # Bas
            (0, -TAILLE_BLOC)    # Haut
        ]
        tete = self.positions[-1]
        mouvements_valides = []
        for mouvement in mouvements_possibles:
            nouvelle_tete = (tete[0] + mouvement[0], tete[1] + mouvement[1])
            if nouvelle_tete in self.positions:
                continue
            if not (ZONE_JEU_X <= nouvelle_tete[0] < ZONE_JEU_X + LARGEUR_ZONE_JEU and
                    ZONE_JEU_Y <= nouvelle_tete[1] < ZONE_JEU_Y + HAUTEUR_ZONE_JEU):
                continue
            mouvements_valides.append(mouvement)
        if not mouvements_valides:
            return "bloque"  # Aucun mouvement valide, l'IA est bloquée
        meilleur_mouvement = min(mouvements_valides,
                            key=lambda mouvement: abs((tete[0] + mouvement[0]) - pomme_x) +
                                                   abs((tete[1] + mouvement[1]) - pomme_y))
        self.direction = meilleur_mouvement
        self.deplacer()
        nouvelle_tete = self.positions[-1]
        if nouvelle_tete[0] == pomme_x and nouvelle_tete[1] == pomme_y:
            self.grandir()
            self.vitesse_ia += 1  # Augmente uniquement la vitesse de l'IA
            return True
        return False


class Jeu:
    """ Classe principale du jeu. """
    def __init__(self):
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption("Jeu Snake")
        self.horloge = pygame.time.Clock()

        self.score = 0
        self.meilleur_score = 0
        self.fin_partie = False
        self.mode = "classique"  # Modes possibles : "classique", "vitesse", "versus"
        self.pause = False
        self.gagne_joueur = False  # Indicateur de victoire du joueur (mode versus)

        # IMPORTANT : le jeu ne démarre qu'après le premier mouvement du joueur.
        self.game_started = False

        self.vitesse_joueur = VITESSE_DEFAUT
        self.dernier_deplacement_joueur = pygame.time.get_ticks()
        self.dernier_deplacement_ia = pygame.time.get_ticks()

        self.serpent_joueur = Snake(self.get_couleur_joueur(), 300, 300)
        self.position_pomme = self.position_aleatoire_pomme()
        self.serpent_ia = None  # Sera initialisé en mode versus

    def get_couleur_joueur(self):
        if self.mode == "classique":
            return COULEUR_CLASSIQUE
        elif self.mode == "vitesse":
            return COULEUR_VITESSE
        elif self.mode == "versus":
            return COULEUR_VERSUS
        return COULEUR_CLASSIQUE

    def position_aleatoire_pomme(self):
        return (
            random.randrange(ZONE_JEU_X + TAILLE_BLOC, ZONE_JEU_X + LARGEUR_ZONE_JEU - TAILLE_BLOC, TAILLE_BLOC),
            random.randrange(ZONE_JEU_Y + TAILLE_BLOC, ZONE_JEU_Y + HAUTEUR_ZONE_JEU - TAILLE_BLOC, TAILLE_BLOC)
        )

    def reinitialiser(self):
        """ Réinitialise l'état du jeu pour une nouvelle partie. """
        self.score = 0
        self.fin_partie = False
        self.gagne_joueur = False
        self.vitesse_joueur = VITESSE_DEFAUT
        self.dernier_deplacement_joueur = pygame.time.get_ticks()
        self.game_started = False  # Réinitialiser le démarrage

        self.serpent_joueur = Snake(self.get_couleur_joueur(), 300, 300)
        self.position_pomme = self.position_aleatoire_pomme()

        if self.mode == "versus":
            self.serpent_ia = AISnake(COULEUR_IA, 350, 350)
            self.dernier_deplacement_ia = pygame.time.get_ticks()
        else:
            self.serpent_ia = None

    def dessiner_zone_jeu(self):
        pygame.draw.rect(self.ecran, COULEUR_BORDURE,
                         (ZONE_JEU_X, ZONE_JEU_Y, LARGEUR_ZONE_JEU, HAUTEUR_ZONE_JEU), 3)

    def dessiner_pomme(self):
        pygame.draw.rect(self.ecran, COULEUR_POMME,
                         (self.position_pomme[0], self.position_pomme[1], TAILLE_BLOC, TAILLE_BLOC))

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                # Dès qu'une touche directionnelle est pressée, on démarre le jeu.
                if not self.game_started:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.game_started = True
                        # On définit la direction initiale en fonction de la touche pressée
                        if event.key == pygame.K_UP:
                            self.serpent_joueur.set_direction((0, -TAILLE_BLOC))
                        elif event.key == pygame.K_DOWN:
                            self.serpent_joueur.set_direction((0, TAILLE_BLOC))
                        elif event.key == pygame.K_LEFT:
                            self.serpent_joueur.set_direction((-TAILLE_BLOC, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.serpent_joueur.set_direction((TAILLE_BLOC, 0))
                if not self.pause:
                    # Les contrôles classiques s'appliquent une fois le jeu démarré
                    if event.key == pygame.K_UP:
                        self.serpent_joueur.set_direction((0, -TAILLE_BLOC))
                    elif event.key == pygame.K_DOWN:
                        self.serpent_joueur.set_direction((0, TAILLE_BLOC))
                    elif event.key == pygame.K_LEFT:
                        self.serpent_joueur.set_direction((-TAILLE_BLOC, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.serpent_joueur.set_direction((TAILLE_BLOC, 0))

    def attendre_debut(self):
        """ Affiche les instructions en overlay sur le jeu et attend qu'une touche directionnelle soit pressée. """
        while not self.game_started:
            # On peut afficher le jeu tel qu'il est (par exemple le fond de jeu)
            self.afficher()  # Affiche le fond, les scores, etc.
            # Affichage des instructions en overlay (texte sans fond)
            self.afficher_texte("Appuyez sur une direction pour commencer", 40, (0, 0, 0),
                                 100, HAUTEUR_ECRAN // 2 - 20)
            self.afficher_texte("Appuyez sur P pour faire pause", 30, (0, 0, 0),
                                 250, HAUTEUR_ECRAN // 2 + 20)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.game_started = True
                        # Définir la direction initiale selon la touche pressée
                        if event.key == pygame.K_UP:
                            self.serpent_joueur.set_direction((0, -TAILLE_BLOC))
                        elif event.key == pygame.K_DOWN:
                            self.serpent_joueur.set_direction((0, TAILLE_BLOC))
                        elif event.key == pygame.K_LEFT:
                            self.serpent_joueur.set_direction((-TAILLE_BLOC, 0))
                        elif event.key == pygame.K_RIGHT:
                            self.serpent_joueur.set_direction((TAILLE_BLOC, 0))
            self.horloge.tick(15)

    def mettre_a_jour(self):
        temps_actuel = pygame.time.get_ticks()
        if not self.pause and not self.fin_partie and self.game_started:
            if temps_actuel - self.dernier_deplacement_joueur >= 1000 / self.vitesse_joueur:
                self.serpent_joueur.deplacer()
                self.dernier_deplacement_joueur = temps_actuel
                tete = self.serpent_joueur.positions[-1]
                if (tete[0] < ZONE_JEU_X or tete[0] >= ZONE_JEU_X + LARGEUR_ZONE_JEU or
                    tete[1] < ZONE_JEU_Y or tete[1] >= ZONE_JEU_Y + HAUTEUR_ZONE_JEU):
                    self.fin_partie = True
                if self.serpent_joueur.se_mord():
                    self.fin_partie = True
                if tete[0] == self.position_pomme[0] and tete[1] == self.position_pomme[1]:
                    self.serpent_joueur.grandir()
                    self.score += 1
                    self.position_pomme = self.position_aleatoire_pomme()
                    if self.mode == "vitesse":
                        self.vitesse_joueur += 2
                    elif self.mode == "versus":
                        self.vitesse_joueur += 1
            if self.serpent_ia is not None:
                if temps_actuel - self.dernier_deplacement_ia >= 1000 / self.serpent_ia.vitesse_ia:
                    resultat = self.serpent_ia.deplacement_ia(self.position_pomme[0], self.position_pomme[1])
                    if resultat == "bloque":
                        self.fin_partie = True
                        self.gagne_joueur = True
                    elif resultat is True:
                        self.position_pomme = self.position_aleatoire_pomme()
                    self.dernier_deplacement_ia = temps_actuel

    def afficher(self):
        background = FONDS[self.mode]
        self.ecran.blit(background, (0, 0))
        self.dessiner_zone_jeu()
        self.dessiner_pomme()
        self.serpent_joueur.afficher(self.ecran)
        if self.serpent_ia is not None:
            self.serpent_ia.afficher(self.ecran)
        self.afficher_texte(f"Score : {self.score}", 30, COULEUR_SCORE, 340, 20)
        if self.mode == "versus" and self.serpent_ia is not None:
            self.afficher_texte(f"Score IA : {self.serpent_ia.longueur - 1}", 30, COULEUR_IA, 340, 60)
        pygame.display.flip()

    def afficher_texte(self, texte, taille, couleur, x, y):
        police = pygame.font.SysFont('Lato', taille)
        surface_texte = police.render(texte, True, couleur)
        self.ecran.blit(surface_texte, (x, y))

    def afficher_menu_pause(self):
        self.ecran.blit(MENU_IMAGE, (0, 0))
        self.afficher_texte("En pause. Appuyez sur P pour reprendre.", 40, (0, 0, 0), 120, 320)
        pygame.display.flip()
        en_pause = True
        while en_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    en_pause = False
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            self.horloge.tick(5)

    def afficher_menu_fin(self):
        if self.score > self.meilleur_score:
            self.meilleur_score = self.score
        self.ecran.blit(MENU_IMAGE, (0, 0))
        if self.gagne_joueur:
            self.afficher_texte("Vous avez gagné !", 50, (0, 0, 0), LARGEUR_ECRAN // 3, HAUTEUR_ECRAN // 3)
        else:
            self.afficher_texte("Fin de partie", 50, (0, 0, 0), LARGEUR_ECRAN // 3, HAUTEUR_ECRAN // 3)
        self.afficher_texte(f"Score : {self.score}", 40, (0, 0, 0), LARGEUR_ECRAN // 3, HAUTEUR_ECRAN // 3 + 50)
        self.afficher_texte(f"Meilleur score : {self.meilleur_score}", 40, (0, 0, 0), LARGEUR_ECRAN // 3, HAUTEUR_ECRAN // 3 + 100)
        if self.mode == "versus" and self.serpent_ia is not None:
            self.afficher_texte(f"Score IA : {self.serpent_ia.longueur - 1}", 40, (0, 0, 0), LARGEUR_ECRAN // 3, HAUTEUR_ECRAN // 3 + 150)
        self.afficher_texte("Appuyez sur R pour rejouer, M pour le menu ou Q pour quitter", 30, (0, 0, 0), 100, HAUTEUR_ECRAN // 3 + 200)
        pygame.display.flip()
        en_attente = True
        while en_attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        en_attente = False; self.reinitialiser()
                    if event.key == pygame.K_m:
                        en_attente = False; Menu(self).afficher_menu()
                    if event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
            self.horloge.tick(5)

    def lancer(self):
        # Attendre que le joueur démarre (avec une touche directionnelle)
        self.attendre_debut()
        while True:
            self.gerer_evenements()
            if self.pause:
                self.afficher_menu_pause()
                self.pause = False
            if self.fin_partie:
                self.afficher_menu_fin()
            self.mettre_a_jour()
            self.afficher()
            self.horloge.tick(FPS_AFFICHAGE)


class Menu:
    """ Classe gérant les menus du jeu (sélection du mode, quitter, etc.). """
    def __init__(self, jeu):
        self.jeu = jeu
        self.ecran = jeu.ecran

    def afficher_menu(self):
        en_cours = True
        while en_cours:
            self.ecran.blit(MENU_IMAGE, (0, 0))
            self.afficher_texte("Choisissez le mode de jeu", 50, (0, 0, 0), LARGEUR_ECRAN // 4, 50)
            boutons = [
                {"texte": "Mode Classique", "rect": pygame.Rect(250, 150, 300, 50), "mode": "classique", "couleur": COULEUR_CLASSIQUE},
                {"texte": "Mode Vitesse Croissante", "rect": pygame.Rect(250, 250, 300, 50), "mode": "vitesse", "couleur": COULEUR_BLEU_CIEL},
                {"texte": "Versus", "rect": pygame.Rect(250, 350, 300, 50), "mode": "versus", "couleur": COULEUR_VERSUS},
                {"texte": "Quitter", "rect": pygame.Rect(250, 450, 300, 50), "mode": "quit", "couleur": (255, 0, 0)}
            ]
            pos_souris = pygame.mouse.get_pos()
            for bouton in boutons:
                rect = bouton["rect"]
                if rect.collidepoint(pos_souris):
                    pygame.draw.rect(self.ecran, (200, 200, 200), rect)
                else:
                    pygame.draw.rect(self.ecran, bouton["couleur"], rect)
                self.afficher_texte(bouton["texte"], 30, (0, 0, 0), rect.x + 20, rect.y + 10)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for bouton in boutons:
                        if bouton["rect"].collidepoint(pos_souris):
                            if bouton["mode"] == "quit":
                                pygame.quit(); sys.exit()
                            else:
                                self.jeu.mode = bouton["mode"]
                                self.jeu.reinitialiser()
                                en_cours = False
            self.jeu.horloge.tick(15)

    def afficher_texte(self, texte, taille, couleur, x, y):
        police = pygame.font.SysFont('Lato', taille)
        surface_texte = police.render(texte, True, couleur)
        self.ecran.blit(surface_texte, (x, y))


# --- LANCEMENT DU JEU ---
if __name__ == "__main__":
    jeu = Jeu()
    Menu(jeu).afficher_menu()
    jeu.lancer()
