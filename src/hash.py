
# Importations
from src.print import *
from src.constantes import *

# Fonctions
def hash_naif(chaine: str|bytes, nb_octets: int = 8) -> int:
    """ Retourne le hash naïf d'une chaine de caractères ou d'octets.\n
    Args:
        chaine (str|bytes): Chaine de caractères ou d'octets à hacher
        nb_octets (int): Nombre d'octets du hash
    Returns:
        int: Hash naïf de la chaine ou des octets

    >>> hash_naif("Hello, world!")
    1161
    >>> hash_naif("Bonjour !")
    800
    >>> hash_naif("bonjour !")
    832
    """
    if isinstance(chaine, str):
        chaine = chaine.encode("utf-8")
    assert isinstance(chaine, bytes), "Les données d'entrée doivent être une chaîne ou des bytes"

    # Hachage naïf (on additionne tous les octets)
    MODULO: int = 2**(8*nb_octets)
    sortie: int = 0
    for octet in chaine:
        sortie = (sortie + octet) % MODULO
    
    # On renvoie la sortie
    return sortie


def hash_sophistique(chaine: str|bytes, nb_octets: int = 8) -> int:
    """ Retourne un hash sophistiqué d'une chaine de caractères ou d'octets.\n
    Args:
        chaine (str|bytes): Chaine de caractères ou d'octets à hacher
        nb_octets (int): Nombre d'octets du hash
    Returns:
        int: Hash sophistiqué de la chaine ou des octets

    Étapes de l'algorithme :
    1. Calcul d'un hash simple (somme des octets) qui servira d'initialisation
    2. Utilisation des décimales de PI et PHI comme source "d'aléatoire" :
       - Sélection d'un index de départ dans PI basé sur le hash simple
       - Sélection d'un index de départ dans PHI basé sur le cube du hash simple (car faut bien quelque chose de différent)
    3. Pour chaque octet de la chaine d'entrée :
       - Utilisation des décimales courantes de PI et PHI pour des opérations arithmétiques
       - Multiplication et division par ces décimales
       - Addition de l'octet multiplié par PI et divisé par PHI
       - Multiplication par un nombre premier (131 car j'ai envie) que je divise par 2
       - Mise à jour des index de PI et PHI de manière bizarre (7 et 31 sont de beaux nombres premiers non ?)
    4. Application d'un modulo final pour obtenir un hash de la taille souhaitée

    Comment m'est venu l'idée ? Et bien au pif, "pourquoi pas utiliser les décimales de PI et PHI ?" et puis j'ai essayé.
    J'ai ensuite testé de changer quelques petits trucs à droites à gauche jusqu'à tous les tests passent.

    >>> hash_sophistique("Hello, world!")
    9718304950604283904
    >>> hash_sophistique("Bonjour !")
    1732255673633341440
    >>> hash_sophistique("bonjour !")
    15120778896696147968
    """
    if isinstance(chaine, str):
        chaine = chaine.encode("utf-8")
    assert isinstance(chaine, bytes), "Les données d'entrée doivent être une chaîne ou des bytes"

    # On calcule un hash très simple qui va servir de base pour le hash sophistiqué
    hash_simple: int = sum(chaine)

    # Les 100 premières décimales de PI (voir constantes.py), on prend un index de départ en fonction du hash simple
    index_de_pi: int = hash_simple % len(DECIMALES_PI)

    # Les 100 premières décimales du nombre d'or (voir constantes.py), on prend un index de départ en fonction du hash simple (au cube)
    index_de_phi: int = (hash_simple**3) % len(DECIMALES_PHI)

    # à ce stade, on a deux index qui déterminent quelle décimale de PI et de PHI on va utiliser
    # On hache la chaine
    MODULO: int = 2**(8*nb_octets)
    sortie: int = 1
    for octet in chaine:
        # On récupère la décimale de PI et PHI correspondante + 1 (pour éviter les divisions par 0)
        decimale_de_pi: int = DECIMALES_PI[index_de_pi] + 1
        decimale_de_phi: int = DECIMALES_PHI[index_de_phi] + 1

        # On fait une multiplication par la décimale de PI et on divise par la décimale de PHI
        sortie = (sortie + (octet * decimale_de_pi) // decimale_de_phi)

        # On ajoute octet multiplié par PHI, on ajoute octet divisé par PHI
        sortie += octet * PI + octet / PHI

        # On multiple par 131, puis on décale de 1 bit vers la droite (division par 2) et on prend le modulo
        sortie = (int(sortie * 131) >> 1) % MODULO

        # On update les index (en ajoutant la valeur de la décimale utilisée de l'autre côté + l'octet)
        index_de_pi = 7*(index_de_pi + decimale_de_phi + octet) % len(DECIMALES_PI)
        index_de_phi = 31*(index_de_phi + decimale_de_pi + octet) % len(DECIMALES_PHI)
    
    return sortie

