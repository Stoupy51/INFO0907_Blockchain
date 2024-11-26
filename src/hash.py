
# Imports
from src.print import *

# Fonctions
@handle_error(exceptions=(ValueError,), error_log=3)
def hash_naif(donnees: str|bytes, taille_sortie: int = 2**32) -> bytes:
	if isinstance(donnees, str):
		donnees = donnees.encode("utf-8")
	assert isinstance(donnees, bytes), "Les données d'entrée doivent être une chaîne ou des bytes"

	# Hachage naïf
	sortie: int = 1
	multiplicateur: int = 1
	for octet in donnees:
		sortie += octet * multiplicateur
		multiplicateur *= 16
	sortie = sortie % taille_sortie

	# On convertit l'entier en bytes
	octets_sortie: bytes = b''
	while sortie > 0:
		octets_sortie = bytes([sortie & 0xFF]) + octets_sortie
		sortie >>= 8
	return octets_sortie

def rangF2(Mat):
    """
    >>> rangF2([[1,1,1,1],[1,0,1,0],[1,1,0,0],[0,1,1,0]])
    3
    >>> rangF2([[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,0,0,0]])
    4
    >>> rangF2([[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,0,0,0]])
    2
    >>> rangF2([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    0
    >>> rangF2([[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]])
    1
    """
    import numpy as np
    M = np.array(Mat, dtype=np.int32) % 2
    nbligne,nbcolonne = M.shape
    rang = 0

    for j in range(nbcolonne):
        iPivot = rang
        while iPivot<nbligne and M[iPivot][j]==0 :
            iPivot+=1

        if (iPivot<nbligne ):
            for j in range(nbcolonne):#On échange les lignes
                M[rang,j],M[iPivot,j]= M[iPivot,j], M[rang,j]
            #On additionne la ligne iPivot aux autres dans F2
            for i in range( iPivot+1,nbligne):
                for j in range( iPivot,nbcolonne):
                    M[i,j]=(M[i,j]+M[iPivot,j])%2
            rang+=1
    return rang

