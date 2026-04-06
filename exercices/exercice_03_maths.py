"""
Exercice 03: Bibliothèque de fonctions mathématiques
Objectif: Maîtriser fonctions, docstrings NumPy, annotations de type
"""

def factorielle(n: int) -> int:
    """
    Calcule le factorielle n de manière récursive

    Parameters
    ----------
    n : int
        Entier positif ou nul


    Returns
    -------
    int
        n! = n * (n-1) * (n-2) * ... * 1, avec 0! = 1


    Raises
    ------
    ValueError
        Si n est négatif


    Examples
    --------
    >>> factorielle(5)
    120

    >>> factorielle(0)
    1
    """
    if n < 0: 
        raise ValueError('n doit être positif ou nul')
    elif n == 0 or n == 1:
        return 1
    elif n >= 2:
        return factorielle(n-1) * n
    


def fibonacci(n: int) -> list:
    """
    Retourne les n premiers termes dans une liste

    Parameters
    ----------
    n: int
        Entier positif ou nul

    
    Returns
    -------
    list
        fibonacci(n) = Liste de n premiers termes

    Raises
    ------
    ValueError
        Si n est négatif


    Examples
    --------
    >>> fibonacci(8)
    [0,1,1,2,3,5,8,13]

    >>> fibonacci(0)
    [0]

    >>> fibonacci(1)
    [0, 1]
    """
    fibo = []
    if n < 0:
        raise ValueError('n doit être un entier positif')
    else:

        for i in range(n+1):
            if i == 0 or i == 1:
                fibo.append(i)
            elif i>1:
                b = fibo[i-2] + fibo[i-1]
                fibo.append(b)

        return fibo


def est_premier(n: int) -> bool:
    """
    Retourne True, si n est un nombre premier

    Sans math.sqrt 


    Parameters
    ----------

    n: int
        Entier positif 

    
    Returns
    -------
    bool
        True, si n est premier, False sinon


    Raises
    ------
    ValueError
        Si n est négatif ou nul


    Examples
    --------

    >>> est_premier(8)
    False

    >>> est_premier(2)
    True

    >>> est_premier(1)
    False
    """

    if n <= 0:
        raise ValueError("n est strictement positif")
    elif n == 1:
        return False
    else:
        for i in range(2, (n//2)+1):
            if n%i == 0:
                return False
        return True


def normaliser(data: list, methode: str = "minmax") -> list:
    """
    Normaliser l'ensemble de données

    methode="minmax" : (x - min) / (max - min)
    methode="zscore" : (x - mean) / std


    Parameters
    ----------
    data: list
        Ensemble des données à normaliser

    methode: str
        La méthode utilisé pour normaliser les données, par défaut "minmax"


    Returns
    -------
    list
        Données normalisées

    
    Examples
    --------
    >>> normaliser([1,2,3,4,5])
    [0.0, 0.25, 0.5, 0.75, 1.0]


    """
    donnees_normalisees = []
    if methode == "minmax":
        minimum = min(data)
        maximum = max(data)
        for x in data:
            valeur_normalisee = (x - minimum) / (maximum-minimum)
            donnees_normalisees.append(valeur_normalisee)

    elif methode == "zscore":
        import math
        n = len(data)
        moyenne = sum(data)/n
        somme_ecart = 0
        for i in data:
            somme_ecart += (i-moyenne)**2
        variance = somme_ecart/n

        ecart_type = math.sqrt(variance)

        for x in data:
            valeur_normalisee = (x - moyenne) / ecart_type
            donnees_normalisees.append(valeur_normalisee)

    return donnees_normalisees
                


if __name__ == "__main__":
    print(factorielle(5))           
    print(fibonacci(1))             
    print(est_premier(1))          
    print(normaliser([1,2,3,4,5]))  