
# Importations
from src.print import *

# Constantes
MSG1: str = "Bonjour les amis !! L'amitié est comme le soleil qui se lève chaque jour… Elle brille sur les relations pour les éclairer de sa lumière naturelle faite d'affection et de tendresse. Je vous souhaite une très bonne journée ! Je vois Je t'envoie ce message pour te souhaiter une agréable journée avec beaucoup de délicatesse et de tendresse. Que chacune des instants de cet jour soit un poème dont la poésie embellit toute chose."
MSG2: str = MSG1.replace("!!", "!")

# Fonction principale
@measure_time(progress)
def main():

	# Hachage des messages
	from hashlib import sha256
	cle1: sha256 = sha256(MSG1.encode("utf-8"))
	cle2: sha256 = sha256(MSG2.encode("utf-8"))
	resultat1: bytes = cle1.digest()
	resultat2: bytes = cle2.digest()

	# Affiche le hachage binaire des messages
	progress("Hachage binaire des messages :", prefix="\n")
	hachage_msg1_binaire: str = "".join(f"{b:08b}" for b in resultat1)
	hachage_msg2_binaire: str = "".join(f"{b:08b}" for b in resultat2)
	info(f"Message 1: {hachage_msg1_binaire}")
	info(f"Message 2: {hachage_msg2_binaire}")

	# Affiche le hachage hexadécimal des messages
	progress("Hachage hexadécimal des messages :", prefix="\n")
	hachage_msg1_hexadecimal: str = "".join(f"{b:02X}" for b in resultat1)
	hachage_msg2_hexadecimal: str = "".join(f"{b:02X}" for b in resultat2)
	info(f"Message 1: {hachage_msg1_hexadecimal}")
	info(f"Message 2: {hachage_msg2_hexadecimal}")

	# Affiche le XOR des hachages
	progress("XOR des hachages (binaire et hexadécimal) :", prefix="\n")
	hachage_xor_binaire: str = "".join(f"{b1^b2:08b}" for b1, b2 in zip(resultat1, resultat2))
	hachage_xor_hexadecimal: str = "".join(f"{b1^b2:02X}" for b1, b2 in zip(resultat1, resultat2))
	info(f"Binaire: {hachage_xor_binaire}")
	info(f"Hexadécimal: {hachage_xor_hexadecimal}")

	return print()

# Point d'entrée du script
if __name__ == "__main__":
	main()

