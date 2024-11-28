
# Importations
from src.print import *
from src.constantes import *
from src.code_prof import rangF2
from src.utils import transformer_en_binaire
from scipy.stats import chisquare
from typing import Iterable
import numpy as np
import itertools
import math


# Fonctions
@handle_error((NotImplementedError,), error_log=0)
def test_frequence(observations: Iterable[int]) -> bool:
    """ Test de la fréquence d'une valeur donnée (f=p+-√n)

    Args:
        observations (Iterable[int]): Distribution observée
    Returns:
        bool: True si le test passe, False sinon
    
    # >>> test_frequence([10, 20, 30])
    # False
    # >>> test_frequence([10, 10, 10])
    # True
    """
    # Assertions
    assert len(observations) > 0, "La distribution observée ne peut être vide"
    somme: int = sum(observations)
    observations = [x/somme for x in observations]

    # Calcul de la fréquence et de l'erreur standard
    frequence: float = sum(observations) / len(observations)
    erreur_standard: float = 1 / math.sqrt(len(observations))

    # On comprend pas pour le moment
    raise NotImplementedError("Nous pas comprendre")



def test_khi2(observations: Iterable[int], esperance: Iterable[int] = [], normaliser: bool = True) -> tuple[bool, float, float]:
    """ Teste le Khi2 entre deux distributions et retourne le résultat.\n
    Le test est passé si la pvalue est supérieure à KHI2_ALPHA (voir src/constantes.py)\n
    pvalue = 1.0 signifie que les distributions sont identiques, le test est donc passé !\n
    tandis que pvalue = 0.0 signifie qu'elles sont complètement différentes

    Args:
        observations  (Iterable[int]):   Distribution observée
        esperance     (Iterable[int]):   Distribution attendue (optionnel, par défaut la distribution uniforme)
        normaliser    (bool):            Normaliser les observations (optionnel, par défaut True)
    Returns:
        bool: True si le test passe, False sinon
        float: statistique du test
        float: pvalue du test
    
    >>> test_khi2([10, 20, 30], [10, 19, 31])
    (True, 0.0014148273910582938, 0.9992928364625473)
    >>> test_khi2([10, 20, 30], [10, 30, 20])
    (False, 0.13888888888888892, 0.9329119603871474)
    >>> test_khi2([97, 93, 88, 81, 76, 73, 71, 66, 65, 64, 64, 58])
    (True, 0.02607820471938775, 0.9999999999998521)
    >>> test_khi2([5, 5], [5, 5])
    (True, 0.0, 1.0)
    >>> test_khi2([1, 1000])
    (False, 0.99600798801598, 0.3182783897943948)
    >>> test_khi2([])
    Traceback (most recent call last):
        ...
    AssertionError: La distribution observée ne peut être vide
    >>> test_khi2([10, 20, 30], [10, 19, 31, 10])
    Traceback (most recent call last):
        ...
    AssertionError: La distribution attendue doit avoir la même longueur que la distribution observée
    """
    assert len(observations) > 0, "La distribution observée ne peut être vide"
    somme_observations: int = sum(observations) # Précalcul de la somme des observations pour optimiser les performances

    # Si l'espérance n'est pas fournie, on la calcule comme une distribution uniforme (genre 1/n partout)
    if len(esperance) == 0 and len(observations) > 0:
        esperance = [somme_observations / len(observations)] * len(observations)
    else:
        assert len(esperance) == len(observations), "La distribution attendue doit avoir la même longueur que la distribution observée"

    # On normalise les observations et l'espérance si on le demande
    if normaliser:
        observations = [o / somme_observations for o in observations]
        esperance = [e / somme_observations for e in esperance]

    # On effectue le test et on retourne le résultat
    khi2: tuple[float, float] = chisquare(observations, esperance)
    return khi2.pvalue > (1 - KHI2_ALPHA), khi2.statistic, khi2.pvalue


def test_rang(observations: Iterable[int]) -> tuple[bool, float, list[int]]:
    """ Teste le rang entre une distribution observée et une distribution uniforme et retourne le résultat.

    Args:
        observations (Iterable[int]): Distribution observée, chaque élément doit être un entier plus petit que 2**64
    Returns:
        bool:      True si le test passe, False sinon
        float:     pvalue du test
        list[int]: Distribution observée
    
    >>> test_rang([10, 20, 30])
    (False, 0.0, [0, 3, 0, 0, 0, 0, 0, 0, 0])
    >>> test_rang([10, 20, 30, 40])
    (False, 0.0, [0, 4, 0, 0, 0, 0, 0, 0, 0])
    >>> test_rang([1, 2, 3, 4, 5, 6])
    (False, 0.0, [0, 6, 0, 0, 0, 0, 0, 0, 0])
    >>> test_rang([""])
    Traceback (most recent call last):
        ...
    AssertionError: Tous les éléments de la distribution observée doivent être des entiers
    >>> test_rang([10, 20, 30, 2**64])
    Traceback (most recent call last):
        ...
    AssertionError: Tous les éléments de la distribution observée doivent être des entiers plus petits que 2**64
    """
    # Assertions
    assert all(isinstance(hash, int) for hash in observations), "Tous les éléments de la distribution observée doivent être des entiers"
    assert all(hash < TWO_POWER_64 for hash in observations), "Tous les éléments de la distribution observée doivent être des entiers plus petits que 2**64"

    # Initialisation des effectifs des rangs à 0
    rangs: list[int] = [0] * len(EXP_RANG)

    # Pour chaque hash, on transforme en binaire, on calcule le rang et on incrémente l'effectif du rang
    for hash in observations:
        matrice_binaire: np.ndarray = transformer_en_binaire(hash)
        rang: int = rangF2(matrice_binaire)
        rangs[rang] += 1

    # Normalisation des effectifs (pour avoir des probas)
    rangs_normalises: list[float] = [i/len(observations) for i in rangs]

    # Test du Khi2
    test_khi2: tuple[float, float] = chisquare(rangs_normalises, EXP_RANG)
    return test_khi2.pvalue > (1 - KHI2_ALPHA), test_khi2.pvalue, rangs


def test_permutation(observations: Iterable[int]) -> tuple[bool, float, float]:
    """ Teste si la distribution des permutations des chiffres des hash suit une loi uniforme.

    Args:
        observations (Iterable[int]): Distribution observée, chaque élément doit être un entier
    Returns:
        bool:  True si le test passe, False sinon
        float: Statistique du test du Khi2
        float: p-value du test du Khi2
    
    >>> test_permutation([123, 132, 213, 231, 312, 321])
    (True, 0.0, 1.0)
    >>> test_permutation([123, 456])
    (False, 5.000000000000003, 0.4158801869955077)
    >>> test_permutation([123, 456, 789])
    (False, 5.000000000000003, 0.4158801869955077)
    >>> test_permutation([])
    Traceback (most recent call last):
        ...
    AssertionError: La liste de hash à tester ne peut être vide
    >>> test_permutation(["123"])
    Traceback (most recent call last):
        ...
    AssertionError: Tous les hash à tester doivent être des entiers
    """
    # Assertions
    assert all(isinstance(hash, int) for hash in observations), "Tous les hash à tester doivent être des entiers"
    assert len(observations) > 0, "La liste de hash à tester ne peut être vide"

    # Recherche du nombre le plus petit parmi les hash car on ne peut comparer les rangs que si ils sont de même longueur
    nb: int = min(len(str(hash)) for hash in observations)
    nb = min(nb, LIMIT_TAILLE_PERMUTATION)

    # Tableau de toutes les permutations possibles
    permutations: list[tuple[int]] = list(itertools.permutations(range(nb), nb))

    # Dictionnaire des effectifs de toutes les permutations possibles
    ordre_effectifs: dict[tuple[int], int] = {key: 0 for key in permutations}

    # Pour chaque hash, on regarde l'ordre des rangs des chiffres
    for hash in observations:
 
        # Séparer chaque chiffre du nombre 
        seperation: list[int] = [int(chiffre) for chiffre in str(hash)]
 
        # Ne prendre que les nb derniers indices  
        seperation = seperation[-nb:]
 
        # Regarder les rangs de chaque chiffre
        rangs: list[int] = np.argsort(np.argsort(seperation))
 
        # On incrémente l'effectif de l'ordre de rangs
        ordre_effectifs[tuple(rangs)] += 1

    # On calcule le test du khi2
    return test_khi2(list(ordre_effectifs.values()), normaliser=True)

