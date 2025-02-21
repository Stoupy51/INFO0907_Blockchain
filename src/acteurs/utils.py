
# Imports
from src.acteurs.config import *
from src.acteurs.Serveur import Serveur
import random

# Functions
def selection_serveur_aleatoire(serveurs: list[Serveur]) -> Serveur:
    """ Selectionne un serveur aléatoire selon la puissance (choix aléatoire pondéré par la puissance)

    Remarque:
    - on aurait pu utiliser np.random.choice(serveurs, p=[x.puissance for x in serveurs])

    Args:
        serveurs    (list[Serveur]):    Liste de serveurs
    Returns:
        Serveur: celui sélectionné au hasard
    
    >>> selection_serveur_aleatoire([])
    Traceback (most recent call last):
        ...
    AssertionError: La liste des serveurs en paramètre ne doit pas être vide
    """
    # Assertions
    assert len(serveurs) > 0, "La liste des serveurs en paramètre ne doit pas être vide"

    # On calcule la puissance total puis on prend aléatoirement dans l'intervalle 
    total_puissance: int = sum(s.puissance for s in serveurs)
    puissance_random: int = random.randint(0, total_puissance)

    # On récupère le serveur choisi et on le renvoie
    # L'idée est de decrémenter jusqu'à être en négatif
    for s in serveurs:
        puissance_random -= s.puissance
        if puissance_random <= 0:
            return s
    return serveurs[0]  # <= Jamais atteint


def puissance_stp(la_range: tuple[int, int, int] = PUISSANCE_RANGE) -> int:
    """ Renvoie (gentiment) une puissance\n
    Args:
        la_range (tuple[int, int, int]): Tuple contenant (min, max, pas)
    Returns:
        int: Une puissance aléatoire dans l'intervalle [min, max] avec le pas
    """
    mini, maxi, pas = la_range
    return random.randrange(mini, maxi + 1, pas)    # max+1 car exclusif


def nouvelle_simulation(nb_serveurs: int = 10, la_range: tuple[int, int, int] = PUISSANCE_RANGE) -> list[Serveur]:
    """ Fonction qui créée une simulation

    Args:
        nb_serveurs (int):   Nombre de serveurs à créer
        la_range    (tuple): La plage de puissance à utiliser
    Returns:
        list[Serveur]:   La liste des serveurs créés
    """
    from src.acteurs.utils import puissance_stp
    
    Serveur.__prochain_id = 1
    return [Serveur(puissance_stp(la_range)) for _ in range(nb_serveurs)]