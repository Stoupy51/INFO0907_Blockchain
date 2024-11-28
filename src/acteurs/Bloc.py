
# Imports
from __future__ import annotations
from src.print import *
from src.constantes import *

# Classe Bloc
class Bloc():
    """ Classe bloc """

    def __init__(self, hash_precedent: str, transactions: list[str], date: int):
        self.hash_precedent: str = hash_precedent
        self.transactions: list[str] = transactions
        self.date: int = date
        self.nonce: str = ""

    @property
    def hash() -> int:
        return 1
    
    def est_valide() -> bool:
        pass


