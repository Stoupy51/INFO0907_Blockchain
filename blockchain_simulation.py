
# Importations
from src.print import *
from src.acteurs import *
from enum import Enum

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
        dict: Rien pour le moment
    """
    for s in serveurs:
        debug(s)
    info(f"Total des puissances : {sum(s.puissance for s in serveurs)}")
    
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
                
    # On retourne les métriques (bidons pour le moment)
    return {"rien":"A FAIRE: une mesure de quelque chose"}


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

