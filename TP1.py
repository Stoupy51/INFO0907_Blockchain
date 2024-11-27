
# Importations
from src.print import *
from src.hash import hash_naif
from src.tests import test_khi2, test_rang, test_permutation
from src.utils import generer_chaines_aleatoires, digest_sha256, conversion_en_int

@measure_time(progress)
def main():
    """ Précalculs (Génération de 10000 chaines random """
    chaines: list[str] = generer_chaines_aleatoires(longueur_mini=64, longueur_maxi=64, nombre_de_chaines=10000)

    """ Partie Astrologie (Test du Khi2, Test de rang) """
    progress("Astrologie", prefix="\n")
    effectifs: list[int] = [97, 93, 88, 81, 76, 73, 71, 66, 65, 64, 64, 58]
    info(f"Test du Khi2:\t{test_khi2(effectifs)}")
    info(f"Test de rang:\t{test_rang(effectifs)}")


    """ Partie SHA256 (Test du Khi2, Test de rang) """
    progress("SHA256 (8 premiers octets)", prefix="\n")
    collection_de_sha256: list[int] = [conversion_en_int(digest_sha256(chaine)[:8]) for chaine in chaines]
    info(f"Test du Khi2:\t{test_khi2(collection_de_sha256)}")
    info(f"Test de rang:\t{test_rang(collection_de_sha256)}")
    info(f"Test de permutation:\t{test_permutation(collection_de_sha256)}")


    """ Partie Hash Naif (Test du Khi2, Test de rang) """
    progress("Hash Naif", prefix="\n")
    collection_de_hash_naif: list[int] = [hash_naif(chaine) for chaine in chaines]
    info(f"Test du Khi2:\t{test_khi2(collection_de_hash_naif)}")
    info(f"Test de rang:\t{test_rang(collection_de_hash_naif)}")
    info(f"Test de permutation:\t{test_permutation(collection_de_hash_naif)}")


    return

if __name__ == "__main__":
    main()

