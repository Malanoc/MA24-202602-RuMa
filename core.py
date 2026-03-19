#============================================================================================================================
# Auteur : Ruben Ten Cate, Marc Schilter
# Date : 26.02.2026
# Description :
# Ce fichier contient toute la logique du jeu Othello.
# Il gère : le plateau, les règles du jeu, les coups possibles, l’application des coups, le calcul du score et une IA simple
#============================================================================================================================


# Taille du plateau (8 lignes et 8 colonnes)
BOARD_SIZE = 8


# Valeurs utilisées dans le tableau
CASE_VIDE = 0
PION_NOIR = 1
PION_BLANC = -1


# Les 8 directions possibles autour d’une case
# (horizontal, vertical, diagonales)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


# ----------------------------------------------------------------------------------
# Création du plateau
# ----------------------------------------------------------------------------------
def creer_plateau():

    plateau = []

    # Création des 8 lignes
    for ligne in range(BOARD_SIZE):

        nouvelle_ligne = []

        # Création des 8 colonnes
        for colonne in range(BOARD_SIZE):
            nouvelle_ligne.append(CASE_VIDE)

        plateau.append(nouvelle_ligne)

    # Placement des 4 pions initiaux au centre
    plateau[3][3] = PION_BLANC
    plateau[4][4] = PION_BLANC
    plateau[3][4] = PION_NOIR
    plateau[4][3] = PION_NOIR

    return plateau

# ----------------------------------------------------------------------------------
# Vérifie si une position est dans le plateau
# ----------------------------------------------------------------------------------
def position_valide(ligne, colonne):

    if ligne >= 0 and ligne < BOARD_SIZE and colonne >= 0 and colonne < BOARD_SIZE:
        return True
    else:
        return False


# ----------------------------------------------------------------------------------
# Trouve les pions à retourner
# ----------------------------------------------------------------------------------
def pions_a_retourner(plateau, ligne, colonne, joueur):

    liste_pions = []

    # Test des 8 directions
    for direction in DIRECTIONS:

        delta_ligne = direction[0]
        delta_colonne = direction[1]

        ligne_courante = ligne + delta_ligne
        colonne_courante = colonne + delta_colonne

        pions_temp = []

        # Avancer tant qu’on trouve des pions adverses
        while position_valide(ligne_courante, colonne_courante) and \
              plateau[ligne_courante][colonne_courante] == -joueur:

            pions_temp.append((ligne_courante, colonne_courante))

            ligne_courante = ligne_courante + delta_ligne
            colonne_courante = colonne_courante + delta_colonne

        # Vérifier si la capture est valide
        if position_valide(ligne_courante, colonne_courante) and \
           plateau[ligne_courante][colonne_courante] == joueur and \
           len(pions_temp) > 0:

            for pion in pions_temp:
                liste_pions.append(pion)

    return liste_pions


# ----------------------------------------------------------------------------------
# Liste des coups possibles
# ----------------------------------------------------------------------------------
def coups_valides(plateau, joueur):

    liste_coups = []

    for ligne in range(BOARD_SIZE):
        for colonne in range(BOARD_SIZE):

            # Vérifier que la case est vide
            if plateau[ligne][colonne] == CASE_VIDE:

                pions = pions_a_retourner(plateau, ligne, colonne, joueur)

                # Si au moins un pion est retourné → coup valide
                if len(pions) > 0:
                    liste_coups.append((ligne, colonne))

    return liste_coups


# ----------------------------------------------------------------------------------
# Applique un coup
# ----------------------------------------------------------------------------------
def jouer_coup(plateau, ligne, colonne, joueur):

    pions = pions_a_retourner(plateau, ligne, colonne, joueur)

    # Coup invalide
    if len(pions) == 0:
        return False

    # Placement du pion
    plateau[ligne][colonne] = joueur

    # Retourner les pions
    for position in pions:
        l = position[0]
        c = position[1]
        plateau[l][c] = joueur

    return True


# ----------------------------------------------------------------------------------
# Calcul du score
# ----------------------------------------------------------------------------------
def calculer_score(plateau):

    score_noir = 0
    score_blanc = 0

    for ligne in plateau:
        for case in ligne:

            if case == PION_NOIR:
                score_noir = score_noir + 1

            if case == PION_BLANC:
                score_blanc = score_blanc + 1

    return score_noir, score_blanc


# ----------------------------------------------------------------------------------
# IA (version utilisée)
# ----------------------------------------------------------------------------------
def trouver_meilleur_coup(plateau, joueur):

    # Choisit le coup qui retourne le plus de pions

    coups = coups_valides(plateau, joueur)

    if len(coups) == 0:
        return None

    # On prend le premier coup comme référence
    meilleur_coup = coups[0]

    max_pions = len(pions_a_retourner(plateau, coups[0][0], coups[0][1], joueur))

    # Comparaison avec les autres coups
    for coup in coups[1:]:

        nb_pions = len(pions_a_retourner(plateau, coup[0], coup[1], joueur))

        if nb_pions > max_pions:
            max_pions = nb_pions
            meilleur_coup = coup

    return meilleur_coup