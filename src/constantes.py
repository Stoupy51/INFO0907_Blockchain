
# Constantes mathématiques
VALEUR_MAX_OCTET: int = 2**8                  # Nombre de valeurs possibles pour un octet
TWO_POWER_64: int = 2**64                     # Nombre de combinaisons possibles pour un 64 bits (on le précalcule car Python ne précalcule pas les puissances (╯°□°)╯︵ ┻━┻)

# Constantes pour les tests statistiques
KHI2_ALPHA: float = 0.05                      # Valeur pour comparer la pvalue du test de Khi2
EXP_RANG: list[float] = [5e-20, 3e-15, 3e-11, 8.6e-08, 4.4e-05, 0.0051, 0.127, 0.578, 0.29] # Effectifs attendus pour le test de rang
EXP_RANG[-1] += 1 - sum(EXP_RANG)             # On ajuste la dernière valeur pour que la somme fasse 1 (car sinon la somme fait 1.000144086030003)
LIMIT_TAILLE_PERMUTATION = 8				  # Taille limite de la suite de chiffres sur laquel on fait le test des permutations pour eviter les problèmes de mémoire quand on calcule toutes les permutations possibles

# Constantes pour la génération de données
SEED: int = 42                                # Seed pour la génération de données
ALPHABET: str = "abcdefghijklmnopqrstuvwxyz"  # Alphabet utilisé pour la génération de chaines aléatoires

# Constantes pour le hash sophistique
PI_STR: str = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
PHI_STR: str = "1.6180339887498948482045868343656381177203091798057628621354486227573744944837797623400665018323050633"
PI: float = float(PI_STR)
PHI: float = float(PHI_STR)
DECIMALES_PI: list[int] = [int(caractere) for caractere in PI_STR[2:] if caractere.isdigit()]
DECIMALES_PHI: list[int] = [int(caractere) for caractere in PHI_STR[2:] if caractere.isdigit()]

