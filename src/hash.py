
# Importations
from src.print import *

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
       - Sélection d'un index de départ dans PHI basé sur le carré du hash simple (car faut bien quelque chose de différent)
    3. Pour chaque octet de la chaine d'entrée :
       - Utilisation des décimales courantes de PI et PHI pour des opérations arithmétiques
       - Multiplication et division par ces décimales
       - Addition de l'octet multiplié par PI et divisé par PHI
       - Multiplication par un nombre premier (131 car j'ai envie)
       - Mise à jour des index de PI et PHI de manière bizarre (7 et 31 sont de beaux nombres premiers non ?)
    4. Application d'un modulo final pour obtenir un hash de la taille souhaitée

    Comment m'est venu l'idée ? Et bien au pif, "pourquoi pas utiliser les décimales de PI et PHI ?" et puis j'ai essayé.

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

    # Les 100 premières décimales de PI, on prend un index de départ en fonction du hash simple
    PI_STR: str = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
    PI: float = float(PI_STR)
    DECIMALES_PI: list[int] = [int(caractere) for caractere in PI_STR[2:] if caractere.isdigit()]
    index_de_pi: int = hash_simple % len(DECIMALES_PI)

    # Les 100 premières décimales du nombre d'or, on prend un index de départ en fonction du hash simple (au carré)
    PHI_STR: str = "1.6180339887498948482045868343656381177203091798057628621354486227573744944837797623400665018323050633"
    PHI: float = float(PHI_STR)
    DECIMALES_PHI: list[int] = [int(caractere) for caractere in PHI_STR[2:] if caractere.isdigit()]
    index_de_phi: int = (hash_simple**2) % len(DECIMALES_PHI)

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

        # On multiple par 131 et on prend le modulo
        sortie = int(sortie * 131) % MODULO

        # On update les index (en ajoutant la valeur de la décimale utilisée de l'autre côté + l'octet)
        index_de_pi = 7*(index_de_pi + decimale_de_phi + octet) % len(DECIMALES_PI)
        index_de_phi = 31*(index_de_phi + decimale_de_pi + octet) % len(DECIMALES_PHI)
    
    return sortie
