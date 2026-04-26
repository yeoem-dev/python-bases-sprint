"""
Exercice 06 : Mini analyseur de dataset — projet intégrateur
=============================================================
Objectif : combiner tous les concepts des exercices 01-05 en une
           classe structurée 

Concepts mobilisés :
    - Ex01 : calcul de moyenne, min, max
    - Ex02 : variance, écart-type, tri, quartiles
    - Ex03 : docstrings NumPy, annotations de type
    - Ex04 : dict comprehensions, groupby, filtrage
    - Ex05 : lecture/écriture CSV, gestion d'erreurs

Auteur  : Emmanuel YÉO
Date    : 2025
Version : 1.0
"""

import csv


# =============================================================================
# Fonctions utilitaires héritées des exercices précédents
# (définies au niveau module pour être réutilisables partout)
# =============================================================================

def _moyenne(valeurs: list) -> float | None:
    """
    Calcule la moyenne d'une liste de nombres.

    Parameters
    ----------
    valeurs : list
        Liste de nombres (float ou int).

    Returns
    -------
    float | None
        La moyenne, ou None si la liste est vide.

    Examples
    --------
    >>> _moyenne([10, 20, 30])
    20.0
    >>> _moyenne([])
    None
    """
    if not valeurs:
        return None
    return sum(valeurs) / len(valeurs)


def _variance(valeurs: list) -> float | None:
    """
    Calcule la variance d'une liste (formule Ex02 : Σ(xᵢ - μ)² / n).

    Parameters
    ----------
    valeurs : list
        Liste de nombres.

    Returns
    -------
    float | None
        La variance, ou None si la liste est vide.
    """
    if not valeurs:
        return None
    mu = _moyenne(valeurs)
    return sum((x - mu) ** 2 for x in valeurs) / len(valeurs)


def _ecart_type(valeurs: list) -> float | None:
    """
    Calcule l'écart-type (racine carrée de la variance).

    Parameters
    ----------
    valeurs : list
        Liste de nombres.

    Returns
    -------
    float | None
        L'écart-type, ou None si la liste est vide.
    """
    v = _variance(valeurs)
    if v is None:
        return None
    # Racine carrée sans math.sqrt — méthode Newton (Ex02)
    if v == 0:
        return 0.0
    x = v
    for _ in range(50):           # convergence rapide en ~10 itérations
        x = (x + v / x) / 2
    return x


def _tri_bulles(valeurs: list) -> list:
    """
    Tri à bulles — réutilisé de l'exercice 02.

    Parameters
    ----------
    valeurs : list
        Liste de nombres à trier.

    Returns
    -------
    list
        Nouvelle liste triée (l'originale n'est pas modifiée).
    """
    data = valeurs.copy()
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    return data


def _mediane(valeurs: list) -> float | None:
    """
    Calcule la médiane d'une liste de nombres.

    Parameters
    ----------
    valeurs : list
        Liste de nombres.

    Returns
    -------
    float | None
        La médiane, ou None si la liste est vide.
    """
    if not valeurs:
        return None
    triee = _tri_bulles(valeurs)
    n = len(triee)
    mid = n // 2
    if n % 2 == 0:
        return (triee[mid - 1] + triee[mid]) / 2
    return float(triee[mid])


# =============================================================================
# Classe principale
# =============================================================================

class DataAnalyzer:
    """
    Mini analyseur de dataset CSV.

    Charge, nettoie, analyse et exporte des données tabulaires.
    Réutilise les fonctions statistiques des exercices 01-05.

    Parameters
    ----------
    chemin_csv : str
        Chemin vers le fichier CSV à analyser.

    Attributes
    ----------
    chemin : str
        Chemin du fichier source.
    donnees : list[dict]
        Données chargées (liste de dictionnaires).
    colonnes : list[str]
        Noms des colonnes détectés à la lecture.

    Examples
    --------
    >>> analyzer = DataAnalyzer("../data/etudiants_clean.csv")
    >>> analyzer.load()
    True
    >>> print(analyzer.rapport())
    """

    def __init__(self, chemin_csv: str):
        self.chemin   = chemin_csv
        self.donnees  = []
        self.colonnes = []

    # -------------------------------------------------------------------------
    # Chargement
    # -------------------------------------------------------------------------

    def load(self) -> bool:
        """
        Charge le fichier CSV en mémoire.

        Utilise csv.DictReader pour obtenir une liste de dicts.
        Gère FileNotFoundError et fichier vide (Ex05).

        Returns
        -------
        bool
            True si le chargement a réussi, False sinon.

        Examples
        --------
        >>> a = DataAnalyzer("inexistant.csv")
        >>> a.load()
        False
        """
        try:
            with open(self.chemin, mode='r', encoding='utf-8') as f:
                lignes = list(csv.DictReader(f))

            if not lignes:
                print(f"Avertissement : '{self.chemin}' est vide.")
                return False

            self.donnees  = lignes
            self.colonnes = list(lignes[0].keys())   # colonnes dynamiques (Ex05)
            print(f"✓ {len(self.donnees)} lignes chargées depuis '{self.chemin}'.")
            return True

        except FileNotFoundError:
            print(f"Erreur : '{self.chemin}' introuvable.")
            return False

    # -------------------------------------------------------------------------
    # Statistiques descriptives
    # -------------------------------------------------------------------------

    def _extraire_numerique(self, colonne: str) -> list[float]:
        """
        Extrait les valeurs numériques valides d'une colonne.

        Convertit en float, ignore les valeurs None ou non convertibles.

        Parameters
        ----------
        colonne : str
            Nom de la colonne à extraire.

        Returns
        -------
        list[float]
            Valeurs numériques valides uniquement.
        """
        valeurs = []
        for ligne in self.donnees:
            val = ligne.get(colonne)
            if val is None:
                continue
            try:
                valeurs.append(float(val))
            except (ValueError, TypeError):
                continue
        return valeurs

    def describe(self) -> dict:
        """
        Calcule les statistiques descriptives de chaque colonne numérique.

        Réutilise _moyenne, _variance, _ecart_type, _mediane (Ex01-02).

        Returns
        -------
        dict
            Dictionnaire {colonne: {count, mean, std, min, median, max}}.
            Seules les colonnes numériques sont incluses.

        Examples
        --------
        >>> stats = analyzer.describe()
        >>> stats["note_ml"]["mean"]
        14.1
        """
        resultats = {}

        for col in self.colonnes:
            valeurs = self._extraire_numerique(col)

            if not valeurs:           # colonne non numérique → on saute
                continue

            triee = _tri_bulles(valeurs)

            resultats[col] = {
                "count"  : len(valeurs),
                "mean"   : round(_moyenne(valeurs),    2),
                "std"    : round(_ecart_type(valeurs), 2),
                "min"    : triee[0],
                "median" : round(_mediane(valeurs),    2),
                "max"    : triee[-1],
            }

        return resultats

    # -------------------------------------------------------------------------
    # Filtrage
    # -------------------------------------------------------------------------

    def filtrer(self, colonne: str, valeur_min: float) -> list:
        """
        Retourne les lignes où colonne >= valeur_min.

        Réutilise le pattern de filtrage par compréhension (Ex04).

        Parameters
        ----------
        colonne : str
            Nom de la colonne sur laquelle filtrer.
        valeur_min : float
            Seuil minimum (inclusif).

        Returns
        -------
        list[dict]
            Lignes satisfaisant la condition.

        Examples
        --------
        >>> admis = analyzer.filtrer("note_ml", 10.0)
        >>> len(admis)
        4
        """
        resultats = []
        for ligne in self.donnees:
            val = ligne.get(colonne)
            try:
                if float(val) >= valeur_min:
                    resultats.append(ligne)
            except (ValueError, TypeError):
                continue         # ignorer silencieusement les valeurs invalides
        return resultats

    # -------------------------------------------------------------------------
    # Groupement
    # -------------------------------------------------------------------------

    def groupby(self, colonne_groupe: str, colonne_valeur: str) -> dict:
        """
        Regroupe par colonne_groupe et calcule la moyenne de colonne_valeur.

        Réutilise le pattern setdefault + _moyenne (Ex04).

        Parameters
        ----------
        colonne_groupe : str
            Colonne servant de clé de regroupement (ex: "ville").
        colonne_valeur : str
            Colonne numérique dont on calcule la moyenne (ex: "note_ml").

        Returns
        -------
        dict
            {groupe: {"count": int, "moyenne": float}}.

        Examples
        --------
        >>> analyzer.groupby("ville", "note_ml")
        {'Paris': {'count': 2, 'moyenne': 13.75}, ...}
        """
        groupes = {}

        for ligne in self.donnees:
            cle = ligne.get(colonne_groupe, "Inconnu")
            val = ligne.get(colonne_valeur)

            # Initialiser le groupe si absent (pattern Ex04)
            groupes.setdefault(cle, [])

            try:
                groupes[cle].append(float(val))
            except (ValueError, TypeError):
                pass          # valeur non numérique → ignorée

        # Dict comprehension pour calculer stats par groupe (Ex04)
        return {
            groupe: {
                "count"  : len(valeurs),
                "moyenne": round(_moyenne(valeurs), 2) if valeurs else None,
            }
            for groupe, valeurs in groupes.items()
        }

    # -------------------------------------------------------------------------
    # Sauvegarde
    # -------------------------------------------------------------------------

    def sauvegarder(self, chemin_sortie: str, lignes: list) -> None:
        """
        Sauvegarde une liste de lignes dans un nouveau fichier CSV.

        Colonnes extraites dynamiquement depuis le premier dict (Ex05).

        Parameters
        ----------
        chemin_sortie : str
            Chemin du fichier CSV de sortie.
        lignes : list[dict]
            Lignes à écrire.

        Returns
        -------
        None

        Examples
        --------
        >>> admis = analyzer.filtrer("note_ml", 10.0)
        >>> analyzer.sauvegarder("../data/admis.csv", admis)
        ✓ 4 lignes sauvegardées dans '../data/admis.csv'.
        """
        if not lignes:
            print("Avertissement : aucune donnée à sauvegarder.")
            return

        # Colonnes dynamiques — jamais codées en dur (leçon Ex05)
        fieldnames = list(lignes[0].keys())

        try:
            with open(chemin_sortie, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(lignes)
            print(f"✓ {len(lignes)} lignes sauvegardées dans '{chemin_sortie}'.")

        except OSError as e:
            print(f"Erreur d'écriture : {e}")

    # -------------------------------------------------------------------------
    # Rapport
    # -------------------------------------------------------------------------

    def rapport(self) -> str:
        """
        Génère un rapport texte formaté avec toutes les statistiques.

        Réutilise describe() et formate façon pandas .describe().

        Returns
        -------
        str
            Rapport multi-lignes prêt à être affiché ou écrit dans un fichier.

        Examples
        --------
        >>> print(analyzer.rapport())
        ========================================
        RAPPORT — ../data/etudiants_clean.csv
        ========================================
        ...
        """
        if not self.donnees:
            return "Aucune donnée chargée. Appeler load() d'abord."

        stats = self.describe()
        sep   = "=" * 50

        # Construction du rapport ligne par ligne (Ex01 : f-strings)
        lignes = [
            sep,
            f"RAPPORT — {self.chemin}",
            f"Lignes totales : {len(self.donnees)}",
            f"Colonnes       : {', '.join(self.colonnes)}",
            sep,
        ]

        for col, s in stats.items():
            lignes.append(f"\n  {col.upper()}")
            lignes.append(f"    count  : {s['count']}")
            lignes.append(f"    mean   : {s['mean']}")
            lignes.append(f"    std    : {s['std']}")
            lignes.append(f"    min    : {s['min']}")
            lignes.append(f"    median : {s['median']}")
            lignes.append(f"    max    : {s['max']}")

        lignes.append(f"\n{sep}")
        return "\n".join(lignes)


# =============================================================================
# Point d'entrée — démonstration complète
# =============================================================================

def _creer_csv_test(chemin: str) -> None:
    """Crée un fichier CSV de test avec des erreurs volontaires."""
    donnees = [
        ["nom",     "age", "note_ml", "note_python", "ville"],
        ["Alice",   "23",  "16.5",    "14",           "Paris"],
        ["Bob",     "25",  "abc",     "12",            "Lyon"],       # note_ml invalide
        ["Claire",  "",    "18",      "19",            "Toulouse"],   # âge manquant
        ["David",   "22",  "11",      "15",            "Paris"],
        ["Emma",    "24",  "14",      "16",            "Lyon"],
        ["Félix",   "21",  "9",       "13",            "Toulouse"],
    ]
    with open(chemin, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(donnees)


if __name__ == "__main__":

    # 0. Créer le fichier de test
    _creer_csv_test("../data/etudiants_raw.csv")

    # 1. Charger
    analyzer = DataAnalyzer("../data/etudiants_raw.csv")
    if not analyzer.load():
        exit(1)

    # 2. Rapport complet
    print(analyzer.rapport())

    # 3. Filtrer les admis en ML (note >= 10)
    admis = analyzer.filtrer("note_ml", 10.0)
    print(f"\nAdmis ML : {len(admis)} étudiant(s)")
    for e in admis:
        print(f"  → {e.get('nom')} : {e.get('note_ml')}")

    # 4. Groupement par ville
    print("\nMoyenne ML par ville :")
    par_ville = analyzer.groupby("ville", "note_ml")
    for ville, info in par_ville.items():
        print(f"  {ville:12} : {info['moyenne']} (n={info['count']})")

    # 5. Sauvegarder les admis
    analyzer.sauvegarder("../data/admis_ml.csv", admis)