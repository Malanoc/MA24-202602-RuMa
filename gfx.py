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
    """
    Initialise la fenêtre pygame et retourne
    l'écran ainsi que la police utilisée.
    """

    pygame.init()

    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # On ajoute 50 pixels pour la zone d'affichage du score
    ecran = pygame.display.set_mode((largeur, hauteur + 50))

    pygame.display.set_caption("Othello")

    police = pygame.font.SysFont(None, 32) # Variable pour la taille de texte (afficher les scores pendant le jeu)
    police_demarrage = pygame.font.SysFont(None, 48) # Variable pour la police de texte dans l'écran de démarrage

    return ecran, police

#Dessine le plateau et les pions.
def dessiner_plateau(ecran, plateau, joueur):

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
    # Dessin des coups possibles pour le joueur actuel

    coups = core.coups_valides(plateau, joueur)

    # Déterminer la couleur des points selon le joueur
    if joueur == core.PION_NOIR:
        couleur_coup = COULEUR_NOIR
    else:
        couleur_coup = COULEUR_BLANC

    for (l, c) in coups:
        x = c * TAILLE_CASE + TAILLE_CASE // 2
        y = l * TAILLE_CASE + TAILLE_CASE // 2

        # Petit cercle de la couleur du joueur
        pygame.draw.circle(ecran, couleur_coup, (x, y), 8)



def dessiner_pion(ecran, centre, rayon, couleur):
    """
    Dessine un pion avec un rendu lisse (anti-aliasing).
    """

    centre_x = centre[0]
    centre_y = centre[1]

    # Cercle rempli
    pygame.gfxdraw.filled_circle(ecran, centre_x, centre_y, rayon, couleur)

    # Contour lisse
    pygame.gfxdraw.aacircle(ecran, centre_x, centre_y, rayon, couleur)


def dessiner_interface(ecran, police, joueur, plateau):
    """
    Affiche le score et indique le joueur actuel.
    """
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

def ecran_demarrage(ecran, police_demarrage):
    """
    Affiche un écran de démarrage et attend un clic pour commencer la partie.
    """

    attente = True
    
    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    # Titre du jeu 

    police_titre = pygame.font.SysFont(None, 80)
    surface_titre = police_titre.render("Jouer à Othello", True, COULEUR_BLANC)
    rect_titre = surface_titre.get_rect(center=(largeur // 2, hauteur // 4))

    # Boutons du menu

    # Bouton 1 : Jouer contre l'IA

    texte_ia = police_demarrage.render("Jouer contre l'IA", True, COULEUR_BLANC)
    rect_ia = texte_ia.get_rect()
    rect_ia.inflate_ip(80, 40)  # Ajouter une marge autour du texte
    rect_ia.center = (largeur // 2, hauteur // 2)

    # Bouton 2 : Jouer contre un ami

    texte_ami = police_demarrage.render("Jouer contre un ami", True, COULEUR_BLANC)
    rect_ami = texte_ami.get_rect()
    rect_ami.inflate_ip(80, 40)  # Ajouter une marge autour du texte
    rect_ami.center = (largeur // 2, hauteur // 2 + 100)


    # Texte de démarrage

    # (code inutile/commenté précédemment, on ne l'affiche plus)

    while attente:
        ecran.fill(COULEUR_PLATEAU)

        # Dessiner le titre
        ecran.blit(surface_titre, rect_titre)

        # Bouton IA
        pygame.draw.rect(ecran, COULEUR_NOIR, rect_ia)
        ecran.blit(texte_ia, texte_ia.get_rect(center=rect_ia.center))

        # Bouton Ami

        pygame.draw.rect(ecran, COULEUR_NOIR, rect_ami)
        ecran.blit(texte_ami, texte_ami.get_rect(center=rect_ami.center))

        pygame.display.flip()
        
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


def choisir_couleur(ecran, police_demarrage):
    """Affiche un écran qui permet au joueur de choisir noir ou blanc."""

    attente = True
    largeur = core.BOARD_SIZE * TAILLE_CASE
    hauteur = core.BOARD_SIZE * TAILLE_CASE

    texte_noir = police_demarrage.render("Jouer Noir", True, COULEUR_BLANC)
    rect_noir = texte_noir.get_rect()
    rect_noir.inflate_ip(80, 40)
    rect_noir.center = (largeur // 2, hauteur // 2)

    texte_blanc = police_demarrage.render("Jouer Blanc", True, COULEUR_BLANC)
    rect_blanc = texte_blanc.get_rect()
    rect_blanc.inflate_ip(80, 40)
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


def ecran_fin(ecran, police, score_noir, score_blanc):

    ecran.fill(COULEUR_PLATEAU)

    if score_noir > score_blanc:
        resultat = "Noir gagne !"
    elif score_blanc > score_noir:
        resultat = "Blanc gagne !"
    else:
        resultat = "Match nul !"

    texte = (
        "Score Final - Noir : " + str(score_noir)
        + "   Blanc : " + str(score_blanc)
        + "   " + resultat
    )

    surface_texte = police.render(texte, True, COULEUR_BLANC)

    position_x = (core.BOARD_SIZE * TAILLE_CASE - surface_texte.get_width()) // 2
    position_y = (core.BOARD_SIZE * TAILLE_CASE - surface_texte.get_height()) // 2

    ecran.blit(surface_texte, (position_x, position_y))

    pygame.display.flip()

    # Attendre un clic pour fermer
    attente = True
    while attente:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                attente = False


