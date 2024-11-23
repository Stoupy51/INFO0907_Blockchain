
# Imports
from src.print import *

# Constants
MSG1: str = "Bonjour les amis !! L’amitié est comme le soleil qui se lève chaque jour… Elle brille sur les relations pour les éclairer de sa lumière naturelle faite d’affection et de tendresse. Je vous souhaite une très bonne journée ! Je vois Je t’envoie ce message pour te souhaiter une agréable journée avec beaucoup de délicatesse et de tendresse. Que chacune des instants de cet jour soit un poème dont la poésie embellit toute chose."
MSG2: str = MSG1.replace("!!", "!")

# Main function
@measure_time(info)
def main():
	# Hash the messages
	from hashlib import sha256
	key1: sha256 = sha256(MSG1.encode("utf-8"))
	key2: sha256 = sha256(MSG2.encode("utf-8"))
	digest1: bytes = key1.digest()
	digest2: bytes = key2.digest()

	# Print the binary hash of the messages
	progress("Binary hash of the messages:")
	hash_msg1_binary: str = "".join(f"{b:08b}" for b in digest1)
	hash_msg2_binary: str = "".join(f"{b:08b}" for b in digest2)
	debug(f"Message 1: {hash_msg1_binary}")
	debug(f"Message 2: {hash_msg2_binary}")

	# Print the hexadecimal hash of the messages
	progress("Hexadecimal hash of the messages:")
	hash_msg1_hexadecimal: str = "".join(f"{b:02X}" for b in digest1)
	hash_msg2_hexadecimal: str = "".join(f"{b:02X}" for b in digest2)
	debug(f"Message 1: {hash_msg1_hexadecimal}")
	debug(f"Message 2: {hash_msg2_hexadecimal}")

	# Print the XOR of the hashes
	progress("XOR of the hashes (binary and hexadecimal):")
	hash_xor_binary: str		= "".join(f"{b1^b2:08b}" for b1, b2 in zip(digest1, digest2))
	hash_xor_hexadecimal: str	= "".join(f"{b1^b2:02X}" for b1, b2 in zip(digest1, digest2))
	debug(f"Binary: {hash_xor_binary}")
	debug(f"Hexadecimal: {hash_xor_hexadecimal}")

	return

# Entry point of the script
if __name__ == "__main__":
	main()

