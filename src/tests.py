
# Importations
from src.print import *
from src.constantes import *
from src.code_prof import rangF2
from src.utils import transformer_en_binaire
from scipy.stats import chisquare
from typing import Iterable
import numpy as np
import itertools


# Fonctions
def test_khi2(observations: Iterable[int], esperance: Iterable[int] = []) -> tuple[bool, float, float]:
    """ Teste le Khi2 entre deux distributions et retourne le résultat.\n
    Le test est passé si la pvalue est inférieure à KHI2_ALPHA (voir src/constantes.py)\n
    pvalue = 1.0 signifie que les distributions sont identiques, tandis que pvalue = 0.0 signifie qu'elles sont complètement différentes

    Args:
        observations  (Iterable[int]):   Distribution observée
        esperance     (Iterable[int]):   Distribution attendue (optionnel, par défaut la distribution uniforme)
    Returns:
        bool: True si le test passe, False sinon
        float: statistique du test
        float: pvalue du test
    
    >>> test_khi2([10, 20, 30], [10, 19, 31])
    (False, 0.08488964346349745, 0.9584433493061473)
    >>> test_khi2([10, 20, 30], [10, 30, 20])
    (True, 8.333333333333334, 0.015503853599009307)
    >>> test_khi2([97, 93, 88, 81, 76, 73, 71, 66, 65, 64, 64, 58])
    (True, 23.366071428571427, 0.01568727481730619)
    >>> test_khi2([])
    Traceback (most recent call last):
        ...
    AssertionError: La distribution observée ne peut être vide
    >>> test_khi2([10, 20, 30], [10, 19, 31, 10])
    Traceback (most recent call last):
        ...
    AssertionError: La distribution attendue doit avoir la même longueur que la distribution observée
    """
    # Si l'espérance n'est pas fournie, on la calcule comme une distribution uniforme (genre 1/n partout)
    if len(esperance) == 0 and len(observations) > 0:
        esperance = [sum(observations) / len(observations)] * len(observations)

    # Assertions
    assert len(observations) > 0, "La distribution observée ne peut être vide"
    assert len(esperance) == len(observations), "La distribution attendue doit avoir la même longueur que la distribution observée"

    # On effectue le test et on retourne le résultat
    khi2: tuple[float, float] = chisquare(observations, esperance)
    return khi2.pvalue < KHI2_ALPHA, khi2.statistic, khi2.pvalue


def test_rang(list_hash_binaire: Iterable[int]) -> tuple[bool, float, list[int]]:
    """ Teste le rang entre une distribution observée et une distribution uniforme et retourne le résultat.

    Args:
        list_hash_binaire (Iterable[int]): Distribution observée, chaque élément doit être un entier plus petit que 2**64
    Returns:
        bool:      True si le test passe, False sinon
        float:     pvalue du test
        list[int]: Distribution observée
    
    >>> test_rang([10, 20, 30])
    (False, 0.0, [0, 3, 0, 0, 0, 0, 0, 0, 0])
    >>> test_rang([10, 20, 30, 40])
    (False, 0.0, [0, 4, 0, 0, 0, 0, 0, 0, 0])
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
    assert all(isinstance(hash, int) for hash in list_hash_binaire), "Tous les éléments de la distribution observée doivent être des entiers"
    assert all(hash < TWO_POWER_64 for hash in list_hash_binaire), "Tous les éléments de la distribution observée doivent être des entiers plus petits que 2**64"

    # Initialisation des effectifs des rangs à 0
    rangs: list[int] = [0] * len(EXP_RANG)

    # Pour chaque hash, on transforme en binaire, on calcule le rang et on incrémente l'effectif du rang
    for hash in list_hash_binaire:
        matrice_binaire: np.ndarray = transformer_en_binaire(hash)
        rang: int = rangF2(matrice_binaire)
        rangs[rang] += 1

    # Normalisation des effectifs (pour avoir des probas)
    rangs_normalises: list[float] = [i/len(list_hash_binaire) for i in rangs]

    # Test du Khi2
    test_khi2: tuple[float, float] = chisquare(rangs_normalises, EXP_RANG)
    return test_khi2.pvalue > 0.05, test_khi2.pvalue, rangs

def test_permutation(list_hash_binaire: Iterable[int]):
    # Assertions
    assert all(isinstance(hash, int) for hash in list_hash_binaire), "Tous les hash à tester doivent être des entiers"
    assert len(list_hash_binaire) > 0, "La liste de hash à tester ne peut être vide"

    #recherche du nombre le plus petit parmi les hash car on ne peut comparer les rangs que si ils sont de même longueur
    nb = min(len(str(hash)) for hash in list_hash_binaire)
    nb = min(nb, LIMIT_TAILLE_PERMUTATION)

    #tableau de toutes les permmutations possibles
    permutations = list(itertools.permutations(range(nb), nb))
    #dictionnaire des effectifs de toutes les permutations possibles
    ordre_effectifs = {key:0 for key in permutations}

    #pour chaque hash, on regarde l'ordre des rangs des chiffres
    for hash in list_hash_binaire:
        #séparer chaque chiffre du nombre 
        sep = [int(chiffre) for chiffre in str(hash)]
        #ne prendre que les nb derniers indices  
        sep = sep[-nb:]
        #regarder les rangs de chaque chiffre
        rangs = np.argsort(np.argsort(sep))
        #on incremente l'effectif de l'ordre de rangs
        ordre_effectifs[tuple(rangs)] +=1
    #on normalise les effectifs
    effectifs_normalises = [value/len(list_hash_binaire) for value in ordre_effectifs.values()]
    #on calcule le test du khi2
    khi2 = test_khi2(effectifs_normalises)
    return khi2



