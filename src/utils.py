
# Importations
from src.constantes import *
from src.print import *
import random
from hashlib import sha256
import numpy as np


# Fonctions
def generer_chaines_aleatoires(longueur_mini: int, longueur_maxi: int, nombre_de_chaines: int, seed: int = SEED) -> list[str]:
    """ Génère une liste de chaines de caractères aléatoires.\n
    Args:
        longueur_mini		(int): Longueur minimale des chaines à générer.
        longueur_maxi		(int): Longueur maximale des chaines à générer.
        nombre_de_chaines	(int): Nombre de chaines à générer.
        seed				(int): Seed pour le générateur aléatoire.
    Returns:
        list[str]: Liste de chaines de caractères aléatoires.

    >>> generer_chaines_aleatoires(4, 4, 3)
    ['bolM', 'Ebem', 'DLKv']
    >>> generer_chaines_aleatoires(4, 4, 3, 1)
    ['DPdg', 'ytkz', 'wNax']
    >>> generer_chaines_aleatoires(20, 20, 1)
    ['bolMJUevblAbkHClEQaP']
    """
    # On applique la seed et on récupère l'alphabet modifié
    random.seed(seed)
    alphabet: str = ALPHABET + ALPHABET.upper()

    # On génère les chaines
    random_letters: list[list[str]] = [
        random.choices(alphabet, k=random.randint(longueur_mini, longueur_maxi))
        for _ in range(nombre_de_chaines)
    ]

    # On retourne les chaines générées
    return [''.join(letters) for letters in random_letters]


def conversion_en_int(chaine: str|bytes) -> int:
    """ Convertit une chaine de caractères ou d'octets en un entier.\n
    Args:
        chaine (str|bytes): Chaine de caractères (ou bytes) à convertir (ex: b'12345678', ou "Bonjour")
    Returns:
        int: Entier converti

    >>> conversion_en_int(b'12345678')
    3544952156018063160
    >>> conversion_en_int("Bonjour")
    18699868485678450
    """
    if isinstance(chaine, str):
        chaine = chaine.encode("utf-8")
    return int.from_bytes(chaine, byteorder="big")


def conversion_int_en_bytes(entier: int, longueur: 8) -> bytes:
    """ Convertit un entier en une chaine d'octets.\n
    Args:
        entier      (int): Entier à convertir
        longueur    (int): Longueur de la chaine d'octets à retourner
    Returns:
        bytes: Chaine d'octets convertie
    
    >>> conversion_int_en_bytes(3544952156018063160, 8)
    b'12345678'
    >>> longueur_chaine: int = len("Bonjour")
    >>> conversion_int_en_bytes(18699868485678450, longueur_chaine).decode("utf-8")
    'Bonjour'
    """
    return entier.to_bytes(longueur, byteorder="big")


def digest_sha256(chaine: str|bytes) -> bytes:
    """ Retourne le digest SHA256 d'une chaine de caractères ou d'octets.\n
    Args:
        chaine (str|bytes): Chaine de caractères ou d'octets à hacher
    Returns:
        bytes: Digest SHA256 de la chaine

    >>> digest_sha256("Bonjour")[:4].hex()
    '9172e8ee'
    >>> digest_sha256("bonjour")[:4].hex()
    '2cb4b143'
    >>> digest_sha256(b'12345678')[:4].hex()
    'ef797c81'
    """
    if isinstance(chaine, str):
        chaine = chaine.encode("utf-8")
    return sha256(chaine).digest()


def transformer_en_binaire(entier: int, taille: int = 8) -> np.ndarray:
    """ Transforme un entier (un hash) en une matrice carrée de taille x 8.\n
    Args:
        entier (int): Entier à transformer en matrice binaire
        taille (int): Taille de la matrice (carrée par défaut: 8)
    Returns:
        np.ndarray: Matrice carrée de taille x 8 contenant la représentation binaire de l'entier

    >>> transformer_en_binaire(3544952156018063160)
    array([[0, 0, 1, 1, 0, 0, 0, 1],
           [0, 0, 1, 1, 0, 0, 1, 0],
           [0, 0, 1, 1, 0, 0, 1, 1],
           [0, 0, 1, 1, 0, 1, 0, 0],
           [0, 0, 1, 1, 0, 1, 0, 1],
           [0, 0, 1, 1, 0, 1, 1, 0],
           [0, 0, 1, 1, 0, 1, 1, 1],
           [0, 0, 1, 1, 1, 0, 0, 0]])
    >>> transformer_en_binaire(0b10110010, taille=1)
    array([[1, 0, 1, 1, 0, 0, 1, 0]])
    """
    # Convertit l'entier en une séquence d'octets
    octets: bytes = entier.to_bytes(taille, byteorder="big")
    
    # Initialise la liste qui contiendra les bits
    matrice_binaire: np.ndarray = np.zeros((taille, 8), dtype=int)

    # Pour chaque octet, on convertit en binaire et on l'ajoute à la matrice
    for i, octet in enumerate(octets):
        # Convertit l'octet en chaine binaire de longueur taille (ex: '00101101')
        bits: str = format(octet, "08b")

        # Convertit chaque caractère '0' ou '1' en entier et l'ajoute comme ligne
        for j, bit in enumerate(bits):
            matrice_binaire[i, j] = int(bit)

    # On renvoie la matrice binaire
    return matrice_binaire


