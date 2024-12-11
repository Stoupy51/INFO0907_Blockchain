
# Imports
from src.acteurs.config import *
from src.acteurs.Serveur import Serveur
import random

# Functions
def selection_serveur_aleatoire(serveurs: list[Serveur]) -> Serveur:
    """ Selectionne un serveur aléatoire selon la puissance

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
    return None


def puissance_stp(la_range: tuple[int, int, int] = PUISSANCE_RANGE) -> int:
    """ Renvoie (gentiment) une puissance\n
    Args:
        la_range (tuple[int, int, int]): Tuple contenant (min, max, pas)
    Returns:
        int: Une puissance aléatoire dans l'intervalle [min, max] avec le pas
    """
    mini, maxi, pas = la_range
    return random.randrange(mini, maxi + 1, pas)    # max+1 car exclusif

