
# Importations
from print import *
import hashlib
import random
import numpy as np
from scipy.stats import chisquare

# Constantes
BYTE_SIZE: int = 256				# Nombre de valeurs possibles pour un octet

# Fonctions
@handle_error(exceptions=(ValueError,), error_log=3)
def test_frequence(donnees: bytes, p: float = 0.5, alpha: float = 0.05) -> tuple[float, bool]:
	""" Test de fréquence (test monobit) pour l'aléatoire (f=p±√n)\n
	Args:
		donnees	(bytes):	Données à tester pour l'aléatoire
		p		(float):	Fréquence attendue de 1 (défaut: 0.5)
		alpha	(float):	Niveau de signification pour le test d'hypothèse (défaut: 0.05)
	Returns:
		tuple[float, bool]: (valeur-p, si le test est passé au niveau de signification alpha)
	Raises:
		ValueError: Si p n'est pas entre 0 et 1, ou si alpha n'est pas entre 0 et 1
	"""
	# Validation des entrées
	assert 0 <= p <= 1, "La fréquence attendue p doit être entre 0 et 1"
	assert 0 <= alpha <= 1, "Le niveau de signification alpha doit être entre 0 et 1"
	assert len(donnees) > 0, "Les données d'entrée ne peuvent pas être vides"

	# Convertir les octets en bits et compter les 1
	bits: str = "".join([f"{octet:08b}" for octet in donnees])
	uns: int = bits.count("1")
	n: int = len(bits)

	# Calculer les fréquences observées et attendues
	freq_observee: float = uns / n
	freq_attendue: float = p

	# Calculer la statistique du test chi-carré et la valeur-p
	f_obs: np.ndarray = np.array([freq_observee, 1 - freq_observee])
	f_exp: np.ndarray = np.array([freq_attendue, 1 - freq_attendue])
	valeur_p: float = chisquare(f_obs, f_exp).pvalue

	# Le test passe si nous ne rejetons pas l'hypothèse nulle
	passe: bool = valeur_p >= alpha
	return valeur_p, passe


# Tester tout
if __name__ == "__main__":
	donnees_test: bytes = bytes(random.randint(0, 255) for _ in range(1000))
	debug(f"Données test: {''.join(f'{b:02X}' for b in donnees_test)[:25]}...")
	info(f"Test de fréquence (p=0.5, alpha=0.05): {test_frequence(donnees_test, p=0.5, alpha=0.05)}")
	pass

