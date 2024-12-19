
# Imports
from __future__ import annotations
from src.print import *
from src.acteurs.config import *
from src.utils import conversion_en_int, conversion_int_en_bytes
from hashlib import sha256
import random

"""
from hashlib import sha256
cle1: sha256 = sha256(MSG1.encode("utf-8"))
cle2: sha256 = sha256(MSG2.encode("utf-8"))
resultat1: bytes = cle1.digest()
resultat2: bytes = cle2.digest()

# Affiche le hachage hex des messages
hachage_msg2_hex: str = "".join(f"{b:02X}" for b in resultat2)
info(f"Message 1: {hachage_msg1_hex}")
"""

# Classe Bloc
class Bloc():
    """ Classe bloc """

    def __init__(self, hash_precedent: str, transactions: list[str], date: int):
        self.hash_precedent: str = hash_precedent
        self.transactions: list[str] = transactions
        self.date: int = date
        self.nonce: int = random.randint(0, NONCE_MAX)

    def hash(self) -> int:
        """ Calcul du hash tu bloc à partir de tous ses éléments concaténé en string, puis calcul d'un sha256 """
        # Chaque élément pris en compte dans le hash
        elements: list = [self.hash_precedent, self.transactions, self.date, self.nonce]

        # Faut plusieurs lignes car là c'est illisible
        octets: bytes = sha256("".join(str(e) for e in elements).encode("utf-8")).digest()
        return conversion_en_int(octets)
    
    def est_valide(self) -> bool:
        """ Regarde si c'est valide """
        # On récupère le hash en hexadécimal
        octets: bytes = conversion_int_en_bytes(self.hash(), longueur=32)
        hex: str = "".join(f"{b:02X}" for b in octets)

        # True si il commence avec le nombre approprié de 0
        return hex.startswith("0" * NB_ZEROS)



