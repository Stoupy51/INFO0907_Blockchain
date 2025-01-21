# Importations
from src.print import *
from src.acteurs import *
from enum import Enum
from collections import Counter
import matplotlib.pyplot as plt

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
            - blockchains: Dictionnaire associant à chaque hash de blockchain sa taille, si elle vient d'un tricheur et le nombre de serveurs l'utilisant
            - taille_max: Taille de la plus longue blockchain
            - puissance_totale: Somme des puissances de calcul
            - historique: Liste des métriques au fil du temps
            - blocs_par_serveur: Nombre de blocs trouvés par chaque serveur
    """
    for s in serveurs:
        debug(s)
    puissance_totale = sum(s.puissance for s in serveurs)
    info(f"Total des puissances : {puissance_totale}")
    
    # Pour tracer les courbes
    historique = {
        "blockchains": [],  # Liste de dictionnaires {hash: {"taille": n, "tricheur": bool}}
        "taille_max": [],
        "temps": []
    }
    temps = 0
    
    # Pour compter les blocs trouvés par serveur
    blocs_par_serveur = {i: 0 for i in range(len(serveurs))}
    
    # Boucle infinie
    while True:
        temps += 1

        # On sélectionne un serveur au hasard
        choisi: Serveur = selection_serveur_aleatoire(serveurs)

        # Il essaie de calculer un bloc
        bloc: Bloc|None = choisi.recherche_bloc()

        # Si trouvé, on l'envoie à tout le monde
        if bloc:
            # On incrémente le compteur pour ce serveur
            blocs_par_serveur[serveurs.index(choisi)] += 1
            
            info(f"[{choisi}] Bloc trouvé et envoyé !")
 
            # On diffuse le message comme quoi le nouvel bloc a été trouvé
            for s in serveurs:
                if s is not choisi:
                    s.recevoir(bloc, choisi, len(choisi.blockchain))
            
            # Mise à jour des métriques pour les courbes
            blockchains_dict = {}
            for s in serveurs:
                if s.blockchain:
                    hash_blockchain = s.blockchain[-1].hash()
                    if hash_blockchain not in blockchains_dict:
                        blockchains_dict[hash_blockchain] = {
                            "taille": len(s.blockchain),
                            "tricheur": False,
                            "nb_serveurs": 0
                        }
                    if s.tricheur:
                        blockchains_dict[hash_blockchain]["tricheur"] = True
            blockchains_dict[hash_blockchain]["nb_serveurs"] += 1
            historique["blockchains"].append(blockchains_dict)
            historique["taille_max"].append(max(len(s.blockchain) for s in serveurs))
            historique["temps"].append(temps)
            
            # Si un des serveurs a plus de 50 blocs, alors stopper
            if condition_darret == ConditionsDarret.PLUS_DE_50_BLOCS:
                if len(choisi.blockchain) >= 50:
                    break

    # On analyse les résultats
    blockchains_dict = {}
    for s in serveurs:
        if s.blockchain:
            hash_blockchain = s.blockchain[-1].hash()
            if hash_blockchain not in blockchains_dict:
                blockchains_dict[hash_blockchain] = {
                    "taille": len(s.blockchain),
                    "tricheur": False,
                    "nb_serveurs": 0
                }
            if s.tricheur:
                blockchains_dict[hash_blockchain]["tricheur"] = True
            blockchains_dict[hash_blockchain]["nb_serveurs"] += 1
    
    taille_max = max(len(s.blockchain) for s in serveurs)
                
    # On retourne les métriques
    return {
        "blockchains": blockchains_dict,
        "taille_max": taille_max,
        "puissance_totale": puissance_totale,
        "historique": historique,
        "blocs_par_serveur": blocs_par_serveur
    }


def plot_simulation_results(result: dict, filename: str):
    """Trace les graphiques des résultats de simulation et les sauvegarde

    Args:
        result (dict): Résultats de la simulation
        filename (str): Nom du fichier pour sauvegarder les graphiques
    """
    historique = result.pop("historique")
    print(result)
    
    try:
        plt.figure(figsize=(15,10))
        
        plt.subplot(221)
        plt.plot(historique["temps"], [len(bc) for bc in historique["blockchains"]])
        plt.title("Évolution du nombre de blockchains")
        plt.xlabel("Temps")
        plt.ylabel("Nombre de blockchains")
        
        plt.subplot(222)
        plt.plot(historique["temps"], historique["taille_max"])
        plt.title("Évolution de la taille maximale")
        plt.xlabel("Temps") 
        plt.ylabel("Nombre de blocs")
        
        plt.subplot(223)
        # Séparer les blockchains honnêtes et malveillantes
        honnetes = 0
        malveillantes = 0
        for info in result["blockchains"].values():
            if info["tricheur"]:
                malveillantes += 1
            else:
                honnetes += 1
                
        labels = ['Honnêtes', 'Malveillantes'] if malveillantes > 0 else ['Honnêtes']
        sizes = [honnetes, malveillantes] if malveillantes > 0 else [honnetes]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title("Répartition des blockchains honnêtes/malveillantes")
        
        plt.subplot(224)
        serveurs_indices = list(result["blocs_par_serveur"].keys())
        blocs_trouves = list(result["blocs_par_serveur"].values())
        plt.bar(serveurs_indices, blocs_trouves)
        plt.title("Nombre de blocs trouvés par serveur")
        plt.xlabel("Numéro du serveur")
        plt.ylabel("Nombre de blocs trouvés")
        
        plt.tight_layout()
        #plt.show()
        plt.savefig(filename)
    except Exception as e:
        warning(f"Erreur lors de la création du graphique: {e}")


@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=0)
def main():
    # Simulation n°1, la plus basique: 10 serveurs sans tricheurs, puissance de calculs aléatoire
    if False:
        print("\n\nSimulation n°1: 10 serveurs sans tricheurs\n")
        NB_SERVEURS: int = 10
        serveurs: list[Serveur] = nouvelle_simulation(NB_SERVEURS)
        result_1: dict = simulation(serveurs)
        plot_simulation_results(result_1, 'simulation_results_1.png')

    # Simulation n°2: ajout d'un tricheur
    if False:
        print("\n\nSimulation n°2: 10 serveurs + 1 tricheur avec 20% de la puissance totale\n")
        NB_SERVEURS: int = 10
        serveurs: list[Serveur] = nouvelle_simulation(NB_SERVEURS - 1)  # 9 serveurs honnêtes
        puissance_totale = sum(s.puissance for s in serveurs)
        # On ajoute un tricheur avec une puissance de calcul élevée
        tricheur = Serveur(puissance=int(20*(puissance_totale/80)), tricheur=True)  # Puissance plus élevée que la normale
        serveurs.append(tricheur)
        result_2: dict = simulation(serveurs)
        plot_simulation_results(result_2, 'simulation_results_2.png')

    # Simulation n°3: ajout d'un tricheur avec une forte puissance de calcul
    if True:
        print("\n\nSimulation n°3: 10 serveurs + 1 tricheur avec 35% de la puissance totale\n")
        NB_SERVEURS: int = 10
        serveurs: list[Serveur] = nouvelle_simulation(NB_SERVEURS - 1)  # 9 serveurs honnêtes
        puissance_totale = sum(s.puissance for s in serveurs)
        # On ajoute un tricheur avec une puissance de calcul élevée
        pourcentage_tricheur: int = 35
        puissance_tricheur: int = int(pourcentage_tricheur*(puissance_totale/(100 - pourcentage_tricheur)))
        tricheur = Serveur(puissance=puissance_tricheur, tricheur=True)
        serveurs.append(tricheur)
        result_3: dict = simulation(serveurs)
        plot_simulation_results(result_3, 'simulation_results_3.png')


if __name__ == "__main__":
    main()

