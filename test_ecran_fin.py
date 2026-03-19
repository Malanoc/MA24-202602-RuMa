import pygame
import gfx
import core

# Initialiser la fenêtre
ecran, police = gfx.initialiser_fenetre()

# Tester avec différents scores
# Noir gagne
print("Test 1 : Noir gagne")
resultat = gfx.ecran_fin(ecran, police, 45, 19)
print(f"Résultat (True=Recommencer, False=Quitter) : {resultat}\n")

# Blanc gagne
print("Test 2 : Blanc gagne")
resultat = gfx.ecran_fin(ecran, police, 20, 44)
print(f"Résultat : {resultat}\n")

# Match nul
print("Test 3 : Match nul")
resultat = gfx.ecran_fin(ecran, police, 32, 32)
print(f"Résultat : {resultat}\n")

pygame.quit()
