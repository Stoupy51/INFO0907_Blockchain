
# Imports
from src.print import *
import numpy as np
from scipy.stats import chisquare

# Fonctions
@handle_error(exceptions=(ValueError,), error_log=3)
def hash_naif(donnees: str|bytes, nb_octets: int = 8) -> bytes:
	if isinstance(donnees, str):
		donnees = donnees.encode("utf-8")
	assert isinstance(donnees, bytes), "Les données d'entrée doivent être une chaîne ou des bytes"

	# Hachage naïf
	sortie: int = 1
	for octet in donnees:
		sortie += octet
	sortie = sortie % (2**(8*nb_octets))

	# On convertit l'entier en bytes
	octets_sortie: bytes = b''
	for i in range(nb_octets):
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

def transformer_en_binaire(entree: bytes) -> list[list[int]]:
    binaire: list[int] = []
    for byte in entree:
        binaire.append(list(map(int,format(byte, '08b'))))
    return binaire

def test_rang(list_hash_binaire: bytes):
    """
    """
    rangs = [0]*9
    #pour chaque hash
    for hash in list_hash_binaire:
        #transformer en binaire
        hash = transformer_en_binaire(hash)
        #debug(hash)
        #transformer en matrice carré 8*8
        hash = np.array(hash).reshape(8,8)
        #appeler la fonction rang
        rang = rangF2(hash)
        #+1 sur les effectifs
        rangs[rang]+=1
    # normaliser les effectifs
    rangs = [i/len(list_hash_binaire) for i in rangs]
    #test du khi2
    #effectifs attendus
    exp = [5e-20, 3e-15, 3e-11, 8.6e-08, 4.4e-05, 0.0051, 0.127, 0.578, 0.29]
    exp[-1] += 1 - sum(exp)
    test_khi2 = chisquare(rangs, exp)
    return test_khi2.pvalue > 0.05, test_khi2.pvalue, rangs



