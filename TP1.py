
# Imports
from src.print import *
from scipy.stats import chisquare
import numpy as np

# Constantes
ALPHA: float = 0.05		# Valeur pour comparer la pvalue
SIGNES: list[str] = ["Gémeaux", "Balance", "Vierge", "Cancer", "Bélier", "Taureau", "Sagittaire", "Poissons", "Verseau", "Lion", "Scorpion", "Capricorne"]
EFFECTIFS: list[int] = [97, 93, 88, 81, 76, 73, 71, 66, 65, 64, 64, 58]

def transformer_en_binaire(entree: int) -> list[int]:
	binaire: list[int] = []
	while entree > 0:
		binaire.append(entree & 1)
		entree = entree >> 1
	return binaire

def test_rang(list_hash_binaire):
	#créer un tableau des rangs avec effectifs à 0
	#pour chaque hash 
	#	transformer en binaire si pas fait
	#	transformer en matrice carré 4*4
	#	appeler la fonction rang 
	#	+1 sur les effectifs
	rangs: list[int] = [0] * 12




@measure_time(progress)
def main():

	# Test du Khi2 sur l'astrologie
	exp = np.array([sum(EFFECTIFS) / len(SIGNES)] * len(SIGNES))
	test_khi2 = chisquare(EFFECTIFS, exp)
	statistique: float = test_khi2.statistic
	pvalue: float = test_khi2.pvalue
	info(f"Statistiques du test du Khi2: {statistique}")
	if pvalue < ALPHA:
		warning(f"Ne passe pas le test de Khi2: {pvalue=}")
	else:
		info(f"Passe le test du Khi2: {pvalue=}")
	
	# Test d'une fonction naive de hachage
	from src.hash import hash_naive
	text1: str = "Bonjour !"
	text2: str = "bonjour !"
	hash1: bytes = hash_naive(text1)
	hash2: bytes = hash_naive(text2)
	info(f"Hash de '{text1}': {hash1.hex()}")
	info(f"Hash de '{text2}': {hash2.hex()}")

	return

if __name__ == "__main__":
	main()

