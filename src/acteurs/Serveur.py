# Importations
from __future__ import annotations
from src.print import *
from src.acteurs.config import *
from src.acteurs.Bloc import Bloc

# Classe
class Serveur():
    """ Classe serveur """
    __prochain_id: int = 1

    # Fonctions de base
    def __init__(self, puissance: int, tricheur: bool = False):
        self.id: int = Serveur.prochain_id()
        self.blockchain: list[Bloc] = []
        self.transactions_a_inserer: list[str] = []
        self.puissance: int = puissance
        self.voisins: list[Serveur] = []
        self.tricheur: bool = tricheur
    
    def __str__(self):
        return f"Server #{self.id:02d}, nb_blocks={len(self.blockchain)}, puissance={self.puissance}"
    
    def afficher_blockchain(self, limit: int = 5) -> None:
        # Début du message
        long: int = len(self.blockchain)
        message: str = f"Longueur de la blockchain: {long}"

        # On ajoute pour chaque bloc son affichage
        borne_inferieur: int = max(0, long - limit)
        for i in range(borne_inferieur, long):
            message += f"\n#{i+1}: {self.blockchain[i]}"

        # Affichage du message
        progress(message)
    
    # Fonctions spécifiques à la classe
    def diffuser(self, message) -> None:
        for voisin in self.voisins:
            voisin.recevoir(message, self, len(self.blockchain), False)
    
    def recevoir(self, bloc: Bloc, emetteur: Serveur, longueur_blockchain: int, rediffuse: bool = False) -> None:
        """ Fonction qui interprète les messages

        Args:
            bloc                (Bloc):     Bloc reçu tout chienplement
            emetteur            (Serveur):  Serveur qui a envoyé le bloc
            longueur_blockchain (int):      Longueur de la blockchain de l'émetteur
            rediffuse           (bool):     Indique si il rediffuse à ses voisins ou non.

        Étapes:
            Vérifie le hash précédent
            Calcul du hash du bloc. Si commence par NB*0, le bloc est bon
            Vérifie la transaction (NotImplemented pour le moment)
            On l'accepte donc
            Il renvoie le bloc à ses voisins car il est gentil (optionnel)
        """
        # Si c'est un tricheur, il ignore les blocs des autres si il n'a pas de blockchain
        if self.tricheur:
            if len(self.blockchain) == 0:
                return
        else:
            # il n'est pas tricheur, il regarde donc comme un bon élève si la blockchain de l'émetteur est 
            # plus longue que sa blockchain
            if longueur_blockchain > len(self.blockchain):
                #demander la blockchain de l'émetteur
                self.blockchain = emetteur.blockchain.copy() # version simplifiée de la réalité

        # On vérifie le hash précédent
        if self.blockchain and self.blockchain[-1].hash() != bloc.hash_precedent:
            return

        # On vérifie la liste de transactions (Pas implementé car pas pertinent dans notre modélisation)
        # if not bloc.transactions:
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
            hash_precedent=(self.blockchain[-1].hash() if self.blockchain else None),
            transactions=self.transactions_a_inserer,
            date=int(time.time())
        )
        if bloc.est_valide():
            self.blockchain.append(bloc)
            return bloc
        return None


    # Fonctions statiques (regarde pas ;-;)
    @staticmethod
    def prochain_id() -> int:
        """ Fonction statique pour récupérer le prochain id et le mettre à jour """
        identifiant: int = Serveur.__prochain_id
        Serveur.__prochain_id += 1
        return identifiant


