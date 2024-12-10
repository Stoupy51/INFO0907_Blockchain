
# Importations
from src.print import *
from src.acteurs import *


@measure_time(progress)
@handle_error((KeyboardInterrupt,), error_log=1)
def main():
    # Création d'une liste de Serveurs
    serveurs: list[Serveur] = [Serveur(puissance_stp()) for _ in range(NB_SERVEURS)]
    for s in serveurs:
        debug(s)
    
    # Boucle infinie
    while True:

        # On sélectionne un serveur au hasard
        choisi: Serveur = selection_serveur_aleatoire(serveurs)

        # Il essaie de calculer un bloc
        bloc: Bloc|None = choisi.recherche_bloc()

        # Si trouvé, on l'envoie à tout le monde
        if bloc:
            info(f"[{choisi}] Bloc trouvé, il l'envoie à tout le monde !")
            for s in serveurs:
                if s is not choisi:
                    s.recevoir(bloc)
    return

if __name__ == "__main__":
    main()

