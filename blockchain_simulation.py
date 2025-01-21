
# Importations
from src.print import *
from src.acteurs import *
from enum import Enum
from collections import Counter

# A FAIRE: 
# introduire des tricheurs 
# regarder le nb de blockchains differentes (hash du dernier bloc)
# faire 1 gros serveur
# puissance de calcul qui monte -> faire graphique ??
# ex à return:
# - nb de blockchains différentes,
# - nb ordinateurs associé à la blockchain malveillante, etc
# MEMORISER ??? puis faire la courbe

class ConditionsDarret(Enum):
    PLUS_DE_50_BLOCS: int = 1


def simulation(
    serveurs: list[Serveur],
    condition_darret: ConditionsDarret = ConditionsDarret.PLUS_DE_50_BLOCS
) -> dict:
    """ Lance une simulation avec les serveurs et la condition d'arrêt donnée

    Args:
        serveurs            (list[Serveur]):    Liste des serveurs à utiliser
        condition_darret    (ConditionsDarret): Condition d'arrêt à utiliser
    Returns:
        dict: Métriques de la simulation:
            - nb_blockchains: Nombre de blockchains différentes à la fin
            - taille_max: Taille de la plus longue blockchain
            - puissance_totale: Somme des puissances de calcul
            - repartition: Répartition des serveurs par blockchain
    """
    for s in serveurs:
        debug(s)
    puissance_totale = sum(s.puissance for s in serveurs)
    info(f"Total des puissances : {puissance_totale}")
    
    # Boucle infinie
    while True:

        # On sélectionne un serveur au hasard
        choisi: Serveur = selection_serveur_aleatoire(serveurs)

        # Il essaie de calculer un bloc
        bloc: Bloc|None = choisi.recherche_bloc()

        # Si trouvé, on l'envoie à tout le monde
        if bloc:
            info(f"[{choisi}] Bloc trouvé et envoyé !")
 
            # TODO Affichage de debug qui est en plein milieu il a rien demandé le pauvre
            if choisi is serveurs[0]:
                choisi.afficher_blockchain()
 
            # On diffuse le message comme quoi el nouvel bloc a été trouvé
            for s in serveurs:
                if s is not choisi:
                    s.recevoir(bloc)
            
            # Si un des serveurs a plus de 50 blocs, alors stopper
            if condition_darret == ConditionsDarret.PLUS_DE_50_BLOCS:
                if len(s.blockchain) > 50:
                    break

    # On analyse les résultats
    blockchains = [s.blockchain[-1].hash() if s.blockchain else None for s in serveurs]
    repartition = Counter(blockchains)
    taille_max = max(len(s.blockchain) for s in serveurs)
                
    # On retourne les métriques
    return {
        "nb_blockchains": len(repartition),
        "taille_max": taille_max,
        "puissance_totale": puissance_totale,
        "repartition": dict(repartition)
    }


@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=0)
def main():

    # Simulation n°1, la plus basique: 10 serveurs sans tricheurs, puissance de calculs aléatoire
    NB_SERVEURS: int = 10
    serveurs: list[Serveur] = nouvelle_simulation(NB_SERVEURS)
    result_1: dict = simulation(serveurs)
    print(result_1)


if __name__ == "__main__":
    main()

