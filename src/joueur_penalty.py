
PAS = 0.01

class Joueur:
    """
    Classe pour simuler un joueur (tireur ou gardien) dans la simulation de penalty
    """
    def __init__(self,proba):
        self.proba = proba
        self.score = 0
        self.direction = 1
        
    def adapter(self,nouveau_score):
        """
        Adapte la probabilité (a ou b) en fonction du gain obtenu
        """
        if nouveau_score < self.score:
            self.direction *= -1
        self.proba += self.direction * PAS
        if self.proba < 0:
            self.proba = 0
        if self.proba > 1:
            self.proba = 1
        self.score = nouveau_score

