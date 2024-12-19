
# Importations
from __future__ import annotations
from src.print import *
from src.acteurs.config import *
from src.acteurs.Bloc import Bloc

# Classe
class Serveur():
    """ Classe serveur """
    __prochain_id: int = 0

    # Fonctions de base
    def __init__(self, puissance: int):
        self.id: int = Serveur.prochain_id()
        self.blockchain: list[Bloc] = []
        self.transactions_a_inserer: list[str] = []
        self.puissance: int = puissance
        self.voisins: list[Serveur] = []
    
    def __str__(self):
        return f"Serveur #{self.id}, {len(self.blockchain)=}, {self.puissance=}"


    # Fonctions spécifiques à la classe
    def diffuser(self, message) -> None:
        for voisin in self.voisins:
            voisin.receive(message)
    
    def recevoir(self, bloc: Bloc, rediffuse: bool = False) -> None:
        """ Fonction qui interprète les messages

        Args:
            bloc        (Bloc):     Bloc reçu tout chienplement
            rediffuse   (bool):     Indique si il rediffuse à ses voisins ou non.

        Étapes:
            Vérifie le hash précédent
            Calcul du hash du bloc. Si commence par NB*0, le bloc est bon
            Vérifie la transaction (NotImplemented pour le moment)
            On l'accepte donc
            Il renvoie le bloc à ses voisins car il est gentil (optionnel)
        """
        # On vérifie le hash précédent
        if self.blockchain and self.blockchain[-1].hash() != bloc.hash_precedent:
            return

        # On vérifie la liste de transactions
        # if not bloc.transactions: # Pas implementé
        #    return

        # On vérifie si le hash du bloc est valide
        if not bloc.est_valide():
            return
        
        # Tous les tests sont passés, on ajoute le bloc
        self.blockchain.append(bloc)
        if rediffuse:
            self.diffuser(bloc)
        return

    def recherche_bloc(self) -> Bloc|None:
        """ Fonction qui recherche un bloc """
        bloc = Bloc(
            hash_precedent=self.blockchain[-1].hash() if self.blockchain else None, 
            transactions=self.transactions_a_inserer,
            date=int(time.time())
        )
        if bloc.est_valide():
            return bloc
        return None


    # Fonctions statiques (regarde pas ;-;)
    @staticmethod
    def prochain_id() -> int:
        """ Fonction statique pour récupérer le prochain id et le mettre à jour """
        identifiant: int = Serveur.__prochain_id
        Serveur.__prochain_id += 1
        return identifiant



