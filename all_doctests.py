
"""
Script permettant d'exécuter tous les tests doctests présents dans les modules du package src.

Le script:
1. Importe dynamiquement tous les modules du package src
2. Exécute les tests doctests de chaque module
3. Affiche une ligne d'erreur éventuelle, pour chaque module, à la fin du script
"""

# Importations
from src.print import *
from doctest import TestResults, testmod
from types import ModuleType
import importlib
import pkgutil
import src

def test_module_avec_progress(module: ModuleType) -> TestResults:
    """ Teste un module et affiche le temps d'exécution """
    @measure_time(progress, message=f"Le test du module '{module.__name__}'\ta pris")
    def interne():
        return testmod(m=module)
    return interne()

# Programme principal
if __name__ == "__main__":

    # Import dynamiquement tous les modules du package src grâce à pkgutil et importlib
    modules: list[ModuleType] = []
    for _, name, _ in pkgutil.iter_modules(src.__path__):
        try:
            module: ModuleType = importlib.import_module(f"src.{name}")
            modules.append(module)
        except ImportError:
            warning(f"Impossible d'importer le module src.{name}")

    # Exécute les tests pour chaque module
    resultats: list[TestResults] = [test_module_avec_progress(module) for module in modules]

    # Affiche une ligne d'erreur éventuelle pour chaque module à la fin du script
    for resultat in resultats:
        if resultat.failed > 0:
            error(f"Erreurs dans le module {module.__name__}", exit=False)

