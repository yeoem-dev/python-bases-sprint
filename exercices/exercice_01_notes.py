"""
Exercice 01: Analyseur de notes d'étudiants
Objectif: Pratiquer variables, types, conditions, boucles simples; fonctions

Auteur  : Emmanuel YÉO
Date    : 2025
Version : 1.0
"""

notes = [12, 17, 8, 14, 19, 11, 15, 6, 18, 13, 5, 10]

# Calculer la moyenne 
if len(notes) >= 1:
    moyenne = sum(notes)/len(notes)
    

# Trouver le min et le max (sans min() ni max())
note_min = notes[0]
note_max = notes[0]


for note in notes:
    if note_min > note:
        note_min = note

    if note_max < note:
        note_max = note



# Compter les étudiants ayant la moyenne (>= 10)
compteur = 0
for i in range(len(notes)):
    if notes[i] >= 10:
        compteur += 1
    

# Attribuer une mention selon la note
def get_mention(note):
    if note >= 0 and note < 10:
        print("Insuffisant") 
    elif note >= 10 and note <= 12:
        print("Passable") 
    elif note > 12 and note <= 14:
        print("Assez-bien")
    elif note > 14 and note <= 16:
        print("Bien")
    elif note > 16 and note <= 20:
        print("Trés-Bien")  




# Afficher un rapport formaté avec f-strings
print(f"Moyenne: {moyenne:.2f} | La note la plus faible: {note_min} | La note la plus haute: {note_max}")