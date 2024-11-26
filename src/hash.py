
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
    modulo: int = 2**(8*nb_octets)
    sortie: int = 0
    for octet in chaine:
        sortie = (sortie + octet) % modulo
    
    # On renvoie la sortie
    return sortie

