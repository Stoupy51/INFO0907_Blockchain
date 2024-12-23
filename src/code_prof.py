
# Importations
import numpy as np

def rangF2(Mat):
    """
    >>> rangF2([[1,1,1,1],[1,0,1,0],[1,1,0,0],[0,1,1,0]])
    3
    >>> rangF2([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])   # Votre code Monsieur ne fonctionnait pas car c'était un copié collé de l'exemple en dessous, j'ai donc utilisé la matrice identité
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

