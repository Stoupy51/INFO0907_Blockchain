
# Importations
from src.print import *
from src.joueur_penalty import *
import random

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
@handle_error((KeyboardInterrupt,), error_log=1)
def main():
    # On initialise les joueurs
    alpha: float = 0.80
    beta: float = 0.40
    alpha: float = 2/7
    beta: float = 4/7
    gardien = Joueur(proba=alpha)
    tireur = Joueur(proba=beta)

    # Listes pour les historiques
    alpha_historique: list = []
    beta_historique: list = []

    # Boucle infinie
    import time
    for _ in range(nb_etapes):
        #time.sleep(1)

        total_gardien, total_tireur = simulation(1000, gardien, tireur)
        gardien.adapter(total_gardien)
        alpha_historique.append(gardien.proba)

        total_gardien, total_tireur = simulation(1000, gardien, tireur)
        tireur.adapter(total_tireur)        
        info(f"Alpha = {gardien.proba:.3f},\tBeta = {tireur.proba:.3f}")
        beta_historique.append(tireur.proba)

    #construction graphique
    import matplotlib.pyplot as plt
    plt.plot(alpha_historique, label="Alpha")
    plt.plot(beta_historique, label="Beta")
    plt.legend()
    plt.savefig("graphique.png")
    
    return

if __name__ == "__main__":
    main()

