#======================================================================================================
# Auteur : Ruben Ten Cate, Marc Schilter
# Date : 26.02.2026
# Description :
# Ce fichier gère toute la partie graphique du jeu Othello avec Pygame.
# Il contient :
# - l'affichage du plateau
# - le dessin des pions
# - les écrans (menu, choix, fin de partie)
#======================================================================================================

import pygame
import pygame.gfxdraw
import core


# Taille d'une case du plateau en pixels
TAILLE_CASE = 90


# Définition des couleurs utilisées dans le jeu
COULEUR_PLATEAU = (20, 110, 20)
COULEUR_NOIR = (30, 30, 30)
COULEUR_BLANC = (245, 245, 245)
COULEUR_LIGNES = (0, 0, 0)


# ----------------------------------------------------------------------------------
# Initialisation de la fenêtre
# ----------------------------------------------------------------------------------
def initialiser_fenetre():

   # Initialise la fenêtre pygame et retourne :
   # l'écran (surface principale)
   # la police pour afficher le texte


    pygame.init()

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # +50 pixels pour afficher le score en bas
    ecran = pygame.display.set_mode((largeur, hauteur + 50))

    pygame.display.set_caption("Othello")

    # Police utilisée pour le score
    police = pygame.font.SysFont(None, 32)

    # Police utilisée dans les menus
    police_demarrage = pygame.font.SysFont(None, 48)

    return ecran, police


# ----------------------------------------------------------------------------------
# Dessin du plateau et des pions
# ----------------------------------------------------------------------------------
def dessiner_plateau(ecran, plateau, joueur):

    # Remplir le fond avec la couleur verte
    ecran.fill(COULEUR_PLATEAU)

    # Parcours de toutes les cases du plateau
    for ligne in range(core.BOARD_SIZE):
        for colonne in range(core.BOARD_SIZE):

            # Calcul de la position en pixels
            position_x = colonne * TAILLE_CASE
            position_y = ligne * TAILLE_CASE

            rectangle = pygame.Rect(
                position_x,
                position_y,
                TAILLE_CASE,
                TAILLE_CASE
            )

            # Dessin de la grille
            pygame.draw.rect(ecran, COULEUR_LIGNES, rectangle, 1)

            # Dessin des pions (si la case n'est pas vide)
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

    # ------------------------------
    # Affichage des coups possibles
    # ------------------------------

    coups = core.coups_valides(plateau, joueur)

    # Couleur des indicateurs selon le joueur
    if joueur == core.PION_NOIR:
        couleur_coup = COULEUR_NOIR
    else:
        couleur_coup = COULEUR_BLANC

    for (l, c) in coups:
        x = c * TAILLE_CASE + TAILLE_CASE // 2
        y = l * TAILLE_CASE + TAILLE_CASE // 2

        # Petit cercle indiquant un coup possible
        pygame.draw.circle(ecran, couleur_coup, (x, y), 8)


# ----------------------------------------------------------------------------------
# Dessin d’un pion (avec anti-aliasing)
# ----------------------------------------------------------------------------------
def dessiner_pion(ecran, centre, rayon, couleur):

    #Dessine un pion rond avec un rendu lisse.
    centre_x = centre[0]
    centre_y = centre[1]

    # Cercle rempli
    pygame.gfxdraw.filled_circle(ecran, centre_x, centre_y, rayon, couleur)

    # Contour lissé
    pygame.gfxdraw.aacircle(ecran, centre_x, centre_y, rayon, couleur)


# ----------------------------------------------------------------------------------
# Interface (score + joueur actuel)
# ----------------------------------------------------------------------------------
def dessiner_interface(ecran, police, joueur, plateau):

    # Calcul du score
    score_noir, score_blanc = core.calculer_score(plateau)

    # Détermination du joueur actuel
    if joueur == core.PION_NOIR:
        texte_joueur = "Noir"
    else:
        texte_joueur = "Blanc"

    # Création du texte
    texte = (
        "Noir : " + str(score_noir)
        + "   Blanc : " + str(score_blanc)
        + "   Tour : " + texte_joueur
    )

    # Transformation en surface graphique
    surface_texte = police.render(texte, True, COULEUR_LIGNES)

    # Position du texte (en bas du plateau)
    position_y = core.BOARD_SIZE * TAILLE_CASE + 10

    ecran.blit(surface_texte, (10, position_y))


# ----------------------------------------------------------------------------------
# Écran de démarrage
# ----------------------------------------------------------------------------------
def ecran_demarrage(ecran, police_demarrage):

    attente = True

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # Titre
    police_titre = pygame.font.SysFont(None, 80)
    surface_titre = police_titre.render("Jouer à Othello", True, COULEUR_BLANC)
    rect_titre = surface_titre.get_rect(center=(largeur // 2, hauteur // 4))

    # Bouton IA
    texte_ia = police_demarrage.render("Jouer contre l'IA", True, COULEUR_BLANC)
    rect_ia = pygame.Rect(0, 0, 300, 60)
    rect_ia.center = (largeur // 2, hauteur // 2)

    # Bouton Ami
    texte_ami = police_demarrage.render("Jouer contre un ami", True, COULEUR_BLANC)
    rect_ami = pygame.Rect(0, 0, 300, 60)
    rect_ami.center = (largeur // 2, hauteur // 2 + 100)

    while attente:
        ecran.fill(COULEUR_PLATEAU)

        # Dessin du titre
        ecran.blit(surface_titre, rect_titre)

        # Boutons
        pygame.draw.rect(ecran, COULEUR_NOIR, rect_ia)
        ecran.blit(texte_ia, texte_ia.get_rect(center=rect_ia.center))

        pygame.draw.rect(ecran, COULEUR_NOIR, rect_ami)
        ecran.blit(texte_ami, texte_ami.get_rect(center=rect_ami.center))

        pygame.display.flip()

        # Gestion des clics
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if rect_ia.collidepoint(pos):
                    return "ia"

                if rect_ami.collidepoint(pos):
                    return "ami"


# ----------------------------------------------------------------------------------
# Choix de la couleur (mode IA)
# ----------------------------------------------------------------------------------
def choisir_couleur(ecran, police_demarrage):

    attente = True

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # Bouton Noir
    texte_noir = police_demarrage.render("Jouer Noir", True, COULEUR_BLANC)
    rect_noir = pygame.Rect(0, 0, 250, 60)
    rect_noir.center = (largeur // 2, hauteur // 2)

    # Bouton Blanc
    texte_blanc = police_demarrage.render("Jouer Blanc", True, COULEUR_BLANC)
    rect_blanc = pygame.Rect(0, 0, 250, 60)
    rect_blanc.center = (largeur // 2, hauteur // 2 + 100)

    while attente:
        ecran.fill(COULEUR_PLATEAU)

        pygame.draw.rect(ecran, COULEUR_NOIR, rect_noir)
        ecran.blit(texte_noir, texte_noir.get_rect(center=rect_noir.center))

        pygame.draw.rect(ecran, COULEUR_NOIR, rect_blanc)
        ecran.blit(texte_blanc, texte_blanc.get_rect(center=rect_blanc.center))

        pygame.display.flip()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if rect_noir.collidepoint(pos):
                    return core.PION_NOIR

                if rect_blanc.collidepoint(pos):
                    return core.PION_BLANC


# ----------------------------------------------------------------------------------
# Écran de fin de partie
# ----------------------------------------------------------------------------------
def ecran_fin(ecran, police, score_noir, score_blanc):

    attente = True

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    police_demarrage = pygame.font.SysFont(None, 48)
    police_score = pygame.font.SysFont(None, 64)

    ecran.fill(COULEUR_PLATEAU)

    # Titre
    police_titre = pygame.font.SysFont(None, 80)
    surface_titre = police_titre.render("Fin du Jeu", True, COULEUR_BLANC)
    rect_titre = surface_titre.get_rect(center=(largeur // 2, hauteur // 8))

    # Détermination du gagnant
    if score_noir > score_blanc:
        resultat = "Noir gagne !"
        couleur_resultat = COULEUR_NOIR
    elif score_blanc > score_noir:
        resultat = "Blanc gagne !"
        couleur_resultat = COULEUR_BLANC
    else:
        resultat = "Match nul !"
        couleur_resultat = COULEUR_LIGNES

    # Affichage du résultat
    surface_resultat = police_demarrage.render(resultat, True, couleur_resultat)
    rect_resultat = surface_resultat.get_rect(center=(largeur // 2, hauteur // 3))

    # Affichage des scores
    surface_score_noir = police_score.render(str(score_noir), True, COULEUR_NOIR)
    rect_score_noir = surface_score_noir.get_rect(center=(largeur // 4, hauteur // 2))

    surface_score_blanc = police_score.render(str(score_blanc), True, COULEUR_BLANC)
    rect_score_blanc = surface_score_blanc.get_rect(center=(3 * largeur // 4, hauteur // 2))

    # Labels pour les scores
    surface_label_noir = police_demarrage.render("Noir", True, COULEUR_NOIR)
    rect_label_noir = surface_label_noir.get_rect(center=(largeur // 4, hauteur // 2 + 60))

    surface_label_blanc = police_demarrage.render("Blanc", True, COULEUR_BLANC)
    rect_label_blanc = surface_label_blanc.get_rect(center=(3 * largeur // 4, hauteur // 2 + 60))

    # Bouton Recommencer
    texte_recommencer = police_demarrage.render("Recommencer", True, COULEUR_BLANC)
    rect_recommencer = pygame.Rect(0, 0, 250, 60)
    rect_recommencer.center = (largeur // 2, hauteur - 100)

    # Bouton Quitter Jeu
    texte_quitter = police_demarrage.render("Quitter", True, COULEUR_BLANC)
    rect_quitter = pygame.Rect(0, 0, 250, 60)
    rect_quitter.center = (largeur // 2, hauteur - 30)

    while attente:
        ecran.fill(COULEUR_PLATEAU)

        # Dessin du titre
        ecran.blit(surface_titre, rect_titre)

        # Dessin du résultat
        ecran.blit(surface_resultat, rect_resultat)

        # Dessin des scores
        ecran.blit(surface_score_noir, rect_score_noir)
        ecran.blit(surface_score_blanc, rect_score_blanc)

        # Dessin des labels
        ecran.blit(surface_label_noir, rect_label_noir)
        ecran.blit(surface_label_blanc, rect_label_blanc)

        # Dessin des boutons
        pygame.draw.rect(ecran, COULEUR_NOIR, rect_recommencer)
        ecran.blit(texte_recommencer, texte_recommencer.get_rect(center=rect_recommencer.center))

        pygame.draw.rect(ecran, COULEUR_NOIR, rect_quitter)
        ecran.blit(texte_quitter, texte_quitter.get_rect(center=rect_quitter.center))

        pygame.display.flip()

        # Gestion des clics
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if rect_recommencer.collidepoint(pos):
                    return True

                if rect_quitter.collidepoint(pos):
                    return False