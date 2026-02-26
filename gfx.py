#======================================================================================================
#Auteur : Ruben Ten Cate, Marc Schilter
#Date : 26.02.2026
#Présentation du programme : Programme du jeu Othello avec une interface graphique utilisant Pygame.
# Le code gère la logique du jeu, les interactions utilisateur et l'affichage du plateau et des pions.
#======================================================================================================
import pygame
import pygame.gfxdraw
import core

# Taille d'une case en pixels
TAILLE_CASE = 90

# Couleurs utilisées
COULEUR_PLATEAU = (20, 110, 20)
COULEUR_NOIR = (30, 30, 30)
COULEUR_BLANC = (245, 245, 245)
COULEUR_LIGNES = (0, 0, 0)

#Initialise la fenêtre pygame et retourne l'écran ainsi que la police utilisée.
def initialiser_fenetre():

    pygame.init()

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # On ajoute 50 pixels pour la zone d'affichage du score
    ecran = pygame.display.set_mode((largeur, hauteur + 50))

    pygame.display.set_caption("Othello")

    police = pygame.font.SysFont(None, 32)

    return ecran, police

#Dessine le plateau et les pions.
def dessiner_plateau(ecran, plateau):

    # Remplir le fond avec la couleur verte
    ecran.fill(COULEUR_PLATEAU)

    for ligne in range(core.BOARD_SIZE):
        for colonne in range(core.BOARD_SIZE):

            position_x = colonne * TAILLE_CASE
            position_y = ligne * TAILLE_CASE

            rectangle = pygame.Rect(
                position_x,
                position_y,
                TAILLE_CASE,
                TAILLE_CASE
            )

            # Dessin des lignes du plateau
            pygame.draw.rect(ecran, COULEUR_LIGNES, rectangle, 1)

            # Dessin des pions si la case n'est pas vide
            if plateau[ligne][colonne] != core.CASE_VIDE:

                if plateau[ligne][colonne] == core.PION_NOIR:
                    couleur_pion = COULEUR_NOIR
                else:
                    couleur_pion = COULEUR_BLANC

                dessiner_pion(
                    ecran,
                    rectangle.center,
                    TAILLE_CASE // 2 - 10,
                    couleur_pion
                )

#  Dessine un pion avec un rendu lisse (anti-aliasing).
def dessiner_pion(ecran, centre, rayon, couleur):

    centre_x = centre[0]
    centre_y = centre[1]

    # Cercle rempli
    pygame.gfxdraw.filled_circle(ecran, centre_x, centre_y, rayon, couleur)

    # Contour lisse
    pygame.gfxdraw.aacircle(ecran, centre_x, centre_y, rayon, couleur)

#  Affiche le score et indique le joueur actuel.
def dessiner_interface(ecran, police, joueur, plateau):

    score_noir, score_blanc = core.calculer_score(plateau)

    if joueur == core.PION_NOIR:
        texte_joueur = "Noir"
    else:
        texte_joueur = "Blanc"

    texte = (
        "Noir : " + str(score_noir)
        + "   Blanc : " + str(score_blanc)
        + "   Tour : " + texte_joueur
    )

    surface_texte = police.render(texte, True, COULEUR_LIGNES)

    position_y = core.BOARD_SIZE * TAILLE_CASE + 10

    ecran.blit(surface_texte, (10, position_y))
# gfx.py

import pygame
import pygame.gfxdraw
import core

# Taille d'une case en pixels
TAILLE_CASE = 90

# Couleurs utilisées
COULEUR_PLATEAU = (20, 110, 20)
COULEUR_NOIR = (30, 30, 30)
COULEUR_BLANC = (245, 245, 245)
COULEUR_LIGNES = (0, 0, 0)

#Initialise la fenêtre pygame et retourne l'écran ainsi que la police utilisée.
def initialiser_fenetre():

    pygame.init()

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # On ajoute 50 pixels pour la zone d'affichage du score
    ecran = pygame.display.set_mode((largeur, hauteur + 50))

    pygame.display.set_caption("Othello")

    police = pygame.font.SysFont(None, 32)

    return ecran, police

#Dessine le plateau et les pions.
def dessiner_plateau(ecran, plateau):

    # Remplir le fond avec la couleur verte
    ecran.fill(COULEUR_PLATEAU)

    for ligne in range(core.BOARD_SIZE):
        for colonne in range(core.BOARD_SIZE):

            position_x = colonne * TAILLE_CASE
            position_y = ligne * TAILLE_CASE

            rectangle = pygame.Rect(
                position_x,
                position_y,
                TAILLE_CASE,
                TAILLE_CASE
            )

            # Dessin des lignes du plateau
            pygame.draw.rect(ecran, COULEUR_LIGNES, rectangle, 1)

            # Dessin des pions si la case n'est pas vide
            if plateau[ligne][colonne] != core.CASE_VIDE:

                if plateau[ligne][colonne] == core.PION_NOIR:
                    couleur_pion = COULEUR_NOIR
                else:
                    couleur_pion = COULEUR_BLANC

                dessiner_pion(
                    ecran,
                    rectangle.center,
                    TAILLE_CASE // 2 - 10,
                    couleur_pion
                )

#  Dessine un pion avec un rendu lisse (anti-aliasing).
def dessiner_pion(ecran, centre, rayon, couleur):

    centre_x = centre[0]
    centre_y = centre[1]

    # Cercle rempli
    pygame.gfxdraw.filled_circle(ecran, centre_x, centre_y, rayon, couleur)

    # Contour lisse
    pygame.gfxdraw.aacircle(ecran, centre_x, centre_y, rayon, couleur)

#  Affiche le score et indique le joueur actuel.
def dessiner_interface(ecran, police, joueur, plateau):

    score_noir, score_blanc = core.calculer_score(plateau)

    if joueur == core.PION_NOIR:
        texte_joueur = "Noir"
    else:
        texte_joueur = "Blanc"

    texte = (
        "Noir : " + str(score_noir)
        + "   Blanc : " + str(score_blanc)
        + "   Tour : " + texte_joueur
    )

    surface_texte = police.render(texte, True, COULEUR_LIGNES)

    position_y = core.BOARD_SIZE * TAILLE_CASE + 10

    ecran.blit(surface_texte, (10, position_y))
