
# Imports
from src.print import *
from scipy.stats import chisquare
import numpy as np

# Constantes
ALPHA: float = 0.05		# Valeur pour comparer la pvalue
SIGNES: list[str] = ["Gémeaux", "Balance", "Vierge", "Cancer", "Bélier", "Taureau", "Sagittaire", "Poissons", "Verseau", "Lion", "Scorpion", "Capricorne"]
EFFECTIFS: list[int] = [97, 93, 88, 81, 76, 73, 71, 66, 65, 64, 64, 58]





@measure_time(progress)
def main():

	# Test du Khi2 sur l'astrologie
	exp = np.array([sum(EFFECTIFS) / len(SIGNES)] * len(SIGNES))
	test_khi2 = chisquare(EFFECTIFS, exp)
	pvalue: float = test_khi2.pvalue
	if pvalue < ALPHA:
		warning(f"Ne passe pas le test de Khi2: {pvalue=}")
	else:
		info(f"Passe le test du Khi2: {pvalue=}")

	#generation de 10000 chaines random
	import random
	chaines= [''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(70)) for j in range(10000)]
	
	# Test du Khi2 sur SHA256
	# A FAIRE

	# Test d'une fonction naive de hachage
	from src.hash import hash_naif
	text1: str = "Bonjour !"
	text2: str = "bonjour !"
	hash1: bytes = hash_naif(text1)
	hash2: bytes = hash_naif(text2)
	info(f"Hash de '{text1}': {hash1.hex()}")
	info(f"Hash de '{text2}': {hash2.hex()}")

	# Test de rang sur 10000 hash naif
	from src.hash import test_rang
	chaines_hash_naif = [hash_naif(x) for x in chaines]
	good, pvalue, rangs = test_rang(chaines_hash_naif)
	print(good)
	print(pvalue)
	print(rangs)
	print()

	# Test de rang sur 10000 hash SHA256
	from hashlib import sha256
	print(test_rang([x[:8] for x in sha10000]))

	return

if __name__ == "__main__":
	main()

