#======================================================================================================
# Auteur : Ruben Ten Cate, Marc Schilter
# Date : 26.02.2026
# Description :
# Programme du jeu Othello avec interface graphique (Pygame).
# Ce fichier gère :
# - le lancement du jeu
# - le choix du mode (joueur vs joueur ou joueur vs IA)
# - la boucle principale
# - les interactions utilisateur
#======================================================================================================

import pygame
import sys
import core
import gfx


# ----------------------------------------------------------------------------------
# Fonction principale : initialise le jeu et choisit le mode
# ----------------------------------------------------------------------------------
def lancer_jeu():

    # Initialisation de la fenêtre graphique
    ecran, police = gfx.initialiser_fenetre()

    # Horloge pour limiter les FPS
    horloge = pygame.time.Clock()

    jeu_continue = True

    # Boucle principale pour permettre de recommencer le jeu
    while jeu_continue:

        # Écran de démarrage : choix du mode de jeu
        mode_jeu = gfx.ecran_demarrage(ecran, police)

        # Création du plateau de départ
        plateau = core.creer_plateau()

        # Le joueur noir commence toujours
        joueur_actuel = core.PION_NOIR

        # ---------------- MODE IA ----------------
        if mode_jeu == "ia":

            # Choix de la couleur du joueur humain
            couleur_humain = gfx.choisir_couleur(ecran, police)

            # L'IA prend la couleur opposée
            couleur_ia = -couleur_humain

            # Lancement du mode contre l'IA
            jeu_continue = lancer_jeu_ia(ecran, police, horloge, plateau, joueur_actuel, couleur_humain, couleur_ia)

        # ---------------- MODE 2 JOUEURS ----------------
        else:
            jeu_continue = lancer_jeu_ami(ecran, police, horloge, plateau, joueur_actuel)

    # Fermeture de pygame à la fin
    pygame.quit()


# ----------------------------------------------------------------------------------
# Mode joueur contre IA
# ----------------------------------------------------------------------------------
def lancer_jeu_ia(ecran, police, horloge, plateau, joueur_actuel, joueur_humain, joueur_ia):

    jeu_en_cours = True

    # Variable utilisée pour créer un délai avant que l'IA joue
    temps_ia = 0

    while jeu_en_cours:

        # Limite à 60 FPS
        horloge.tick(60)

        # Calcul des coups possibles
        liste_coups_valides = core.coups_valides(plateau, joueur_actuel)

        # ----------- Gestion des événements -----------
        for evenement in pygame.event.get():

            # Fermeture de la fenêtre
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Clic souris (uniquement pour le joueur humain)
            if evenement.type == pygame.MOUSEBUTTONDOWN and joueur_actuel == joueur_humain:

                if len(liste_coups_valides) > 0:

                    # Position de la souris
                    position_souris = pygame.mouse.get_pos()
                    position_x = position_souris[0]
                    position_y = position_souris[1]

                    # Conversion en coordonnées du plateau
                    colonne = position_x // gfx.TAILLE_CASE
                    ligne = position_y // gfx.TAILLE_CASE

                    # Vérification du coup
                    if (ligne, colonne) in liste_coups_valides:

                        core.jouer_coup(plateau, ligne, colonne, joueur_actuel)

                        # Changement de joueur
                        joueur_actuel = -joueur_actuel

        # ----------- Tour de l'IA -----------
        if joueur_actuel == joueur_ia:

            liste_coups_valides = core.coups_valides(plateau, joueur_ia)

            if len(liste_coups_valides) > 0:

                # Temps actuel
                temps_actuel = pygame.time.get_ticks()

                # Initialisation du délai
                if temps_ia == 0:
                    temps_ia = temps_actuel

                # Attente de 1.5 secondes
                if temps_actuel - temps_ia >= 1500:

                    # Choix du meilleur coup
                    meilleur_coup = core.trouver_meilleur_coup(plateau, joueur_ia)

                    if meilleur_coup is not None:
                        core.jouer_coup(plateau, meilleur_coup[0], meilleur_coup[1], joueur_ia)

                    joueur_actuel = -joueur_actuel
                    temps_ia = 0  # reset du timer

        # ----------- Gestion des tours impossibles -----------
        if len(liste_coups_valides) == 0:

            joueur_actuel = -joueur_actuel

            # Si aucun joueur ne peut jouer → fin
            if len(core.coups_valides(plateau, joueur_actuel)) == 0:

                jeu_en_cours = False

                score_noir, score_blanc = core.calculer_score(plateau)
                recommencer = gfx.ecran_fin(ecran, police, score_noir, score_blanc)
                return recommencer

        # ----------- Affichage -----------
        gfx.dessiner_plateau(ecran, plateau, joueur_humain)
        gfx.dessiner_interface(ecran, police, joueur_actuel, plateau)

        pygame.display.flip()

    return True


# ----------------------------------------------------------------------------------
# Mode joueur contre joueur
# ----------------------------------------------------------------------------------
def lancer_jeu_ami(ecran, police, horloge, plateau, joueur_actuel):

    jeu_en_cours = True

    while jeu_en_cours:

        horloge.tick(60)

        liste_coups_valides = core.coups_valides(plateau, joueur_actuel)

        for evenement in pygame.event.get():

            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evenement.type == pygame.MOUSEBUTTONDOWN:

                if len(liste_coups_valides) > 0:

                    position_souris = pygame.mouse.get_pos()
                    position_x = position_souris[0]
                    position_y = position_souris[1]

                    colonne = position_x // gfx.TAILLE_CASE
                    ligne = position_y // gfx.TAILLE_CASE

                    if (ligne, colonne) in liste_coups_valides:

                        core.jouer_coup(plateau, ligne, colonne, joueur_actuel)

                        joueur_actuel = -joueur_actuel

        # Gestion des tours impossibles
        if len(liste_coups_valides) == 0:

            joueur_actuel = -joueur_actuel

            if len(core.coups_valides(plateau, joueur_actuel)) == 0:

                jeu_en_cours = False

                score_noir, score_blanc = core.calculer_score(plateau)
                recommencer = gfx.ecran_fin(ecran, police, score_noir, score_blanc)
                return recommencer

        # Affichage
        gfx.dessiner_plateau(ecran, plateau, joueur_actuel)
        gfx.dessiner_interface(ecran, police, joueur_actuel, plateau)

        pygame.display.flip()

    return True


# ----------------------------------------------------------------------------------
# Lancement du programme
# ----------------------------------------------------------------------------------
if __name__ == "__main__":
    lancer_jeu()