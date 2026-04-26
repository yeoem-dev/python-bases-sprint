"""
Exercice 05: Lecture de fichiers CSV avec gestion d'erreurs
Objectif: fichiers, exceptions, robutesse - comme en production

Auteur: Emmanuel YÉO
Date: 2026
version: 1.0

"""

import csv


def moyenne(liste):
        if not liste:
            return None
        return sum(liste)/len(liste)


# Créer un fichier csv de test
def creer_csv_test(chemin: str) -> None:
    """
    Créer un CSV de test

    Parameters
    ----------

    chemin
        str: Le nom du fichier à créer

    
    """

    # des erreurs volontairement classées pour refleter la réalité
    
    donnees = [
        ["nom", "age", "note_ml", "note_python", "ville"],
        ["Alice",  "23", "16.5", "14",   "Paris"],
        ["Bob",    "25", "abc",  "12",   "Lyon"],       
        ["Claire", "",   "18",   "19",   "Toulouse"],  
        ["David",  "22", "11",   "15",   "Paris"],
        ["Emma",   "24", "14",   "16",   "Lyon"],
    ]
    with open(chemin, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(donnees)

# Lire le CSV et retourner une liste de dicts
def lire_csv(chemin: str) -> list:
    """
    Lire un CSV

    Parameters
    ----------

    chemin
        str: Le nom ou le chemin vers le fichier à ouvrir

    
    Returns
    -------
    list: Liste de dictionnaires comprenant des étudiants


    """
    try:
        with open(chemin, mode='r', encoding='utf-8') as lecteur_csv:
            lignes = list(csv.DictReader(lecteur_csv))
            if not lignes:
                print(f"Erreur: '{chemin}' est vide.")
                return []
            return lignes
    except FileNotFoundError:
        print(f"{chemin} n'existe pas ")
        return []



def nettoyer_donnees(donnees: list) -> list:
    """
    Nettoyer les données:
        - Convertir les notes en float (ValueError si invalide -> None)
        - Convertir l'âge en int (ValueError -> None)

    Parameters
    ----------

    donnees
        list: Valeurs d'entrées


    Returns
    -------

    list

    """
    nettoyees = []

    for i, donnee in enumerate(donnees):

        try:
            donnee["age"] = int(donnee["age"])
        except (KeyError, ValueError):
            print(f"Erreur ligne {i+1}, ({donnee.get('age', '?')}) -> age invalide = None")
            donnee["age"] = None

        try:
            donnee["note_python"] = float(donnee["note_python"])
        except (KeyError, ValueError):
            print(f"Erreur ligne {i+1}, ({donnee.get('note_python', '?')}) invalide pour 'age' (attendu: int) → None ")
            donnee["note_python"] = None


        try:
            donnee["note_ml"] = float(donnee["note_ml"])
        except (KeyError, ValueError):
            print(f"Erreur ligne {i+1}, ({donnee.get('note_ml', '?')}) -> invalide pour 'note_ml' (attendu: float) → None")
            donnee["note_ml"] = None   
        
        nettoyees.append(donnee)

    return nettoyees



def analyser(donnees_propres: list) -> dict:
    """
    Filtrer et calculer des stats 

    Parameters
    ----------

    donnees_propres
        list: données propres à calculer

    
    Returns
    -------

        dict


    """
    # Séparer les lignes valides pour chaque métrique
    ages_valides = [d["age"] for d in donnees_propres if d["age"] is not None]
    notes_ml_valides = [d["note_ml"] for d in donnees_propres if d["note_ml"] is not None]

    

    return {
        "total": len(donnees_propres),
        "lignes_valides": len(notes_ml_valides),
        "moyenne_age": round(moyenne(ages_valides), 2) if ages_valides else None,
        "moyenne_ml": round(moyenne(notes_ml_valides), 2) if notes_ml_valides else None,
        "admis_ml": sum(1 for n in notes_ml_valides if n>=10)
    }


def ecrire_csv_propre(donnees: list, chemin_sortie: str) -> None:
    """
    Écrire les données nettoyées dans un nouveau CSV

    Parameters
    ----------

    donnees
        list: Les données nettoyées à enregistrer dans le nouveau CSV

    chemin_sortie
        str: Les données propres enregistrées dans un CSV


    
    """
    if not donnees:
        print('Aucune donnée à écrire.')
        return
    
    fieldnames = list(donnees[0].keys()) # extraire les colonnes du premier dict
    
    with open(chemin_sortie, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(donnees)


if __name__ == "__main__":
    creer_csv_test("../data/etudiants_raw.csv")
    donnees = lire_csv("../data/etudiants_raw.csv")
    print(donnees)
    propres = nettoyer_donnees(donnees)
    stats   = analyser(propres)
    ecrire_csv_propre(propres, "../data/etudiants_clean.csv")
    print(
        f"Total         : {stats['total']}\n"
        f"Lignes valides : {stats['lignes_valides']}\n"
        f"Moyenne âge   : {stats['moyenne_age']}\n"
        f"Moyenne ML    : {stats['moyenne_ml']}\n"
        f"Admis ML      : {stats['admis_ml']}"
    )    