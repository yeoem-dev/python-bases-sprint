"""
Exercice 02: Statistiques descriptives sans librairie
Objectif: Pratiquer boucles, conditions imbriqueées, logique algorithmique
"""

donnees = [23, 45, 12, 67, 34, 89, 56, 11, 78, 42,
           33, 55, 66, 22, 44, 77, 88, 99, 10, 50]

# Moyenne, Variance, écart-type
def calcul_stats(donnees):
    import math

    n = len(donnees)
    moyenne = sum(donnees)/n
    somme_ecart = 0
    for i in donnees:
        somme_ecart += (i-moyenne)**2
    variance = somme_ecart/(n)

    ecart_type = math.sqrt(variance)

    return moyenne, variance, ecart_type




# Implémentation du tri à bulle
def tri_bulle(tab):
    data = tab.copy()
    if len(data) > 1:
        for i in range(len(data)):
            
            for j in range(i):
                if data[i] < data[j]:
                    data[i], data[j] = data[j], data[i]
                   

    return data





def calcul_quartiles(donnees):
    """
    Calculer médiane et quartiles Q1, Q3
    """
    donnees_triees = tri_bulle(donnees)
    N = len(donnees)
    q1 = (N + 3) // 4
    mediane = (N + 1) // 2
    q3 = (3*N + 1) // 4

    return donnees_triees[q1], donnees_triees[mediane], donnees_triees[q3]


# Afficher façon panda .describe()
def describe(donnees):
    moyenne, variance, ecart_type = calcul_stats(donnees)
    q1, mediane, q3 = calcul_quartiles(donnees)
    print(f"Taille des données: {len(donnees)}")
    print(f"Moyenne: {moyenne:.2f} | Variance: {variance:.2f} | Écart-type: {ecart_type:.2f}")
    print(f"Médiane: {mediane} | Q1: {q1} | Q3: {q3}")

# describe(donnees)