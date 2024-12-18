
# Importations
from src.print import *
from src.joueur_penalty import *
import matplotlib.pyplot as plt
import random
import time

# On initialise l1 et l2 (les scores pour chaque cas)
l1: list[int] = [4, 7, 9, 5]
l2: list[int] = [6, 3, 1, 5]
nb_etapes = 10001

def simulation(boucle: int, gardien: Joueur, tireur: Joueur) -> tuple[int,int]:
    total_gardien: int = 0
    total_tireur: int = 0
    for _ in range(boucle):
        if random.random() < gardien.proba:
            if random.random() < tireur.proba:
                total_gardien += l1[0]
                total_tireur += l2[0]
            else:
                total_gardien += l1[2]
                total_tireur += l2[2]
        else:
            if random.random() < tireur.proba:
                total_gardien += l1[1]
                total_tireur += l2[1]
            else:
                total_gardien += l1[3]
                total_tireur += l2[3]
    return total_gardien, total_tireur


@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=0)
def main():
    # On initialise les joueurs
    alpha: float = 0.70
    beta: float = 0.70
    #alpha: float = 2/7
    #beta: float = 4/7
    gardien = Joueur(proba=alpha)
    tireur = Joueur(proba=beta)

    # Listes pour les historiques
    alpha_historique: list = []
    beta_historique: list = []

    # Boucle infinie
    for i in range(nb_etapes):
        if i%666 == 0:
            progress(f"{(i/nb_etapes)*100:.2f}% (Alpha={gardien.proba:.3f},\tBeta={tireur.proba:.3f})")
        #time.sleep(1)

        total_gardien, total_tireur = simulation(10000, gardien, tireur)
        gardien.adapter(total_gardien)
        alpha_historique.append(gardien.proba)

        total_gardien, total_tireur = simulation(10000, gardien, tireur)
        tireur.adapter(total_tireur)        
        #info(f"Alpha = {gardien.proba:.3f},\tBeta = {tireur.proba:.3f}")
        beta_historique.append(tireur.proba)

    # Construction graphique
    # Calcul de l'opacité (plus un point est vieux, plus il est transparent)
    opacite = [0.1 + 0.9 * i/len(beta_historique) for i in range(len(beta_historique))]
    plt.scatter(beta_historique, alpha_historique, s=1, alpha=opacite)
    plt.xlabel("Beta") 
    plt.ylabel("Alpha")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.savefig("graphique.png")
    
    return

if __name__ == "__main__":
    main()

