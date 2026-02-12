# main.py

import pygame
import sys
import core
import gfx

# Fonction principale qui lance et gère le jeu.



def lancer_jeu():

    # Initialisation de la fenêtre graphique

    ecran, police = gfx.initialiser_fenetre()

    horloge = pygame.time.Clock()

    # Création du plateau initial
    plateau = core.creer_plateau()

    # Joueur IA 
    joueur_humain = core.PION_NOIR
    joueur_ia = core.PION_BLANC

    # Le joueur noir commence toujours
    joueur_actuel = core.PION_NOIR

    jeu_en_cours = True
    
    temps_ia = 0  # Pour gérer le délai de l'IA

    gfx.ecran_demarrage(ecran, police)

    # Boucle principale
    while jeu_en_cours:

        # Limite à 60 images par seconde
        horloge.tick(60)

        # Calcul des coups valides pour le joueur actuel
        liste_coups_valides = core.coups_valides(plateau, joueur_actuel)

        # Gestion des événements (clavier, souris, fermeture)
        for evenement in pygame.event.get():

            # Fermeture de la fenêtre
            if evenement.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Clic de la souris - uniquement si c'est le tour du joueur humain
            if evenement.type == pygame.MOUSEBUTTONDOWN and joueur_actuel == joueur_humain:

                # On vérifie qu'il existe au moins un coup possible
                if len(liste_coups_valides) > 0:

                    position_souris = pygame.mouse.get_pos()

                    position_x = position_souris[0]
                    position_y = position_souris[1]

                    colonne = position_x // gfx.TAILLE_CASE
                    ligne = position_y // gfx.TAILLE_CASE

                    # Vérifier si le coup est valide
                    if (ligne, colonne) in liste_coups_valides:

                        core.jouer_coup(plateau, ligne, colonne, joueur_actuel)

                        # Changement de joueur
                        joueur_actuel = -joueur_actuel

        # Si c'est le tour de l'IA
        if joueur_actuel == joueur_ia:
            
            # Recalculer les coups valides pour l'IA
            liste_coups_valides = core.coups_valides(plateau, joueur_ia)
            
            if len(liste_coups_valides) > 0:
                
                # Délai de 1.5 secondes sans bloquer la boucle
                temps_actuel = pygame.time.get_ticks()
                
                if temps_ia == 0:
                    temps_ia = temps_actuel
                
                if temps_actuel - temps_ia >= 1500:  # 1500 ms = 1.5 secondes
                    
                    meilleur_coup = core.trouver_meilleur_coup(plateau, joueur_ia)
                    
                    if meilleur_coup is not None:
                        core.jouer_coup(plateau, meilleur_coup[0], meilleur_coup[1], joueur_ia)
                    
                    joueur_actuel = -joueur_actuel
                    temps_ia = 0  # Réinitialiser le délai

        # Si aucun coup possible, on passe le tour
        if len(liste_coups_valides) == 0:

            joueur_actuel = -joueur_actuel

            # Si l'autre joueur ne peut pas jouer non plus → fin du jeu
            if len(core.coups_valides(plateau, joueur_actuel)) == 0:
                jeu_en_cours = False

                score_noir, score_blanc = core.calculer_score(plateau)
                gfx.ecran_fin(ecran, police, score_noir, score_blanc)



        # Dessin du plateau
        gfx.dessiner_plateau(ecran, plateau)

        # Dessin de l'interface (score et tour)
        gfx.dessiner_interface(ecran, police, joueur_actuel, plateau)

        pygame.display.flip()

    # Fin du jeu
    pygame.quit()


# Lancement du programme
if __name__ == "__main__":
    lancer_jeu()
