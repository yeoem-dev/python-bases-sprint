"""
Exercice 04: Manipulation avancée de structures de données
Objectif: list/dict comprehensions, imbrication, manipulation réaliste
"""

etudiants = [
    {"nom": "Alice", "notes": [14, 16, 12, 18], "filiere":"Info"},
    {"nom": "Bob", "notes": [9, 11, 8, 10], "filiere":"Maths"},
    {"nom": "Claire", "notes": [17, 15, 19, 16], "filiere":"Info"},
    {"nom": "David", "notes": [7, 9, 11, 8], "filiere":"Physique"},
    {"nom": "Emma", "notes": [13, 14, 15, 12], "filiere":"Maths"},
    {"nom": "Felix", "notes": [18, 17, 20, 19], "filiere":"Info"},
]

# Ajouter la moyenne à chaque étudiant
# Résultat : chaque dict a une clé "moyenne
etudiants_moyenne = [
    {**etudiant, "moyenne": sum(etudiant["notes"]) / len(etudiant["notes"])}
    for etudiant in etudiants
]

# Filtrer les admis (moyenne >= 10)
# Résultat : {"Info": [...], "Maths": [...], "Physique": [...]}
admis = [etudiant["nom"] for etudiant in etudiants_moyenne if etudiant["moyenne"] >= 10]

# Grouper par filière
par_filiere = dict()
for f in etudiants:
    par_filiere[f['filiere']] = []

for filiere in par_filiere:
    for etudiant in etudiants:
        if filiere == etudiant['filiere']:
            par_filiere[filiere].append(etudiant["nom"])

# print(par_filiere)


# Moyenne par filière
# Résultat : {"Info": 17.25, "Maths": 12.25, "Physique": 8.75}
moyenne_filiere = dict()


for p in par_filiere:
    somme = 0
    for etudiant in etudiants_moyenne:
        if etudiant["filiere"] == p:
            somme += etudiant["moyenne"]

    moyenne_filiere[p] = somme / len(par_filiere[p])
    

# print(moyenne_filiere)

# TOP 3 des etudiants
classement = etudiants_moyenne.copy()
for i in range(len(classement)):
    for j in range(i):
        if classement[i]["moyenne"] > classement[j]["moyenne"]:
            classement[i], classement[j] = classement[j], classement[i]

for i in range(3):
    print(f"{i+1}- {(classement[i]["nom"])}")
