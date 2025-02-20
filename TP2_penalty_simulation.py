
# Importations
from src.print import *
from src.joueur_penalty import *
import matplotlib.pyplot as plt
import random
import time

# On initialise l1 et l2 (les scores pour chaque cas)
L1: list[int] = [4, 7, 9, 5]
L2: list[int] = [6, 3, 1, 5]
NB_ETAPES: int = 10001

def simulation(boucle: int, gardien: Joueur, tireur: Joueur) -> tuple[int,int]:
    total_gardien: int = 0
    total_tireur: int = 0
    for _ in range(boucle):
        if random.random() < gardien.proba:
            if random.random() < tireur.proba:
                total_gardien += L1[0]
                total_tireur += L2[0]
            else:
                total_gardien += L1[2]
                total_tireur += L2[2]
        else:
            if random.random() < tireur.proba:
                total_gardien += L1[1]
                total_tireur += L2[1]
            else:
                total_gardien += L1[3]
                total_tireur += L2[3]
    return total_gardien, total_tireur


@measure_time(progress, "Simulation de penalty")
@handle_error((KeyboardInterrupt,Exception), error_log=2)
def main():
    # On initialise les joueurs
    alpha: float = 2/7
    beta: float = 4/7
    gardien = Joueur(proba=alpha)
    tireur = Joueur(proba=beta)

    # Listes pour les historiques
    alpha_historique: list = []
    beta_historique: list = []

    # Boucle de 10000 étapes
    for i in range(NB_ETAPES):
        if i%666 == 0:
            info(f"{(i/NB_ETAPES)*100:.2f}% (Alpha={gardien.proba:.3f},\tBeta={tireur.proba:.3f})")
        #time.sleep(1)

        total_gardien, total_tireur = simulation(100000, gardien, tireur)
        gardien.adapter(total_gardien)
        alpha_historique.append(gardien.proba)

        total_gardien, total_tireur = simulation(100000, gardien, tireur)
        tireur.adapter(total_tireur)        
        #info(f"Alpha = {gardien.proba:.3f},\tBeta = {tireur.proba:.3f}")
        beta_historique.append(tireur.proba)

    # Construction graphique
    # Création d'un histogramme 2D pour visualiser la densité
    plt.hist2d(beta_historique, alpha_historique, bins=50, cmap='viridis', density=True)
    plt.colorbar(label='Densité')
    plt.title("Simulation de penalty - Graphique de densité")
    plt.xlabel("Beta")
    plt.ylabel("Alpha") 
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.savefig("penalty_simulation_densite.png")
    
    return

if __name__ == "__main__":
    main()

