# Python Bases Sprint — 2 jours

> Sprint d'apprentissage Python : maîtriser les fondamentaux en 2 jours
> avec des exercices orientés data science et machine learning.

---

## Objectifs

- Maîtriser variables, types, conditions, boucles, fonctions
- Manipuler listes, dictionnaires, fichiers CSV avec robustesse
- Adopter les bonnes pratiques dès le début : PEP 8, docstrings NumPy, Git workflow
- Poser les bases pour le ML from scratch (semaine suivante : OOP avec Martelli)

---

## Contenu

| # | Fichier | Concept clé | Lien ML |
|---|---------|-------------|---------|
| 01 | `exercice_01_notes.py` | Conditions, boucles, f-strings | Métriques de classification |
| 02 | `exercice_02_stats.py` | Boucles imbriquées, tri à bulles | `StandardScaler` (sklearn) |
| 03 | `exercice_03_maths.py` | Fonctions, docstrings NumPy, annotations | Fonctions utilitaires réutilisables |
| 04 | `exercice_04_donnees.py` | Dict comprehensions, groupby, filtrage | Manipulation Pandas-like |
| 05 | `exercice_05_csv.py` | Fichiers CSV, `try/except`, robustesse | `pandas.read_csv()` |
| 06 | `exercice_06_analyzer.py` | Classe complète, architecture modulaire | Pipeline ML de bout en bout |

---

## Structure du projet

```
python-bases-sprint/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── exercices/
│   ├── exercice_01_notes.py
│   ├── exercice_02_stats.py
│   ├── exercice_03_maths.py
│   ├── exercice_04_donnees.py
│   ├── exercice_05_csv.py
│   └── exercice_06_analyzer.py
│
└── data/
    ├── etudiants_raw.csv      ← généré par exercice_05
    ├── etudiants_clean.csv    ← généré par exercice_05
    └── admis_ml.csv           ← généré par exercice_06
```

---

## Prérequis

```bash
python >= 3.10
```

Aucune librairie externe 

---

## Lancer les exercices

```bash
git clone https://github.com/yeodem-dev/python-bases-sprint.git
cd python-bases-sprint

# Exemple : lancer le projet intégrateur
python exercices/exercice_06_analyzer.py
```

Sortie attendue :

```
✓ 6 lignes chargées depuis 'data/etudiants_raw.csv'.
==================================================
RAPPORT — data/etudiants_raw.csv
Lignes totales : 6
...
✓ 4 lignes sauvegardées dans 'data/admis_ml.csv'.
```

---

## Ce que j'ai appris

**Jour 1**
- Variables, types natifs, opérateurs, f-strings
- Conditions `if/elif/else` imbriquées
- Boucles `for`, `while`, `enumerate()`, `zip()`
- Fonctions avec docstrings NumPy et annotations de type

**Jour 2**
- Listes, dictionnaires, sets — manipulation avancée
- List/dict comprehensions avec conditions
- Lecture et écriture de fichiers CSV (`csv.DictReader`, `csv.DictWriter`)
- Gestion d'erreurs robuste (`try/except` par champ, `FileNotFoundError`)
- Architecture d'une classe Python avec méthodes publiques et privées (`_`)

---

## Concepts clés retenus

```python
# Itérer avec index → enumerate, pas range(len(...))
for i, element in enumerate(liste):
    ...

# Colonnes dynamiques → jamais hardcodées
fieldnames = list(donnees[0].keys())

# Underscore → convention "fonction interne"
def _moyenne(valeurs): ...   # outil interne
def analyser(donnees): ...   # API publique

# Try/except par champ → granularité maximale
try:
    donnee["age"] = int(donnee["age"])
except (ValueError, KeyError):
    donnee["age"] = None
```

