#Hello
"""
Exercise: Write a program to process a file of DNA text, such as:
ATGCAATTGCTCGATTAGATGCBB
ATGCAATTGCTCGATTAGATGCBB
ATCGCGAATTGCTCGATTAGATG

Count the percent of 
C+G OR G+C present in the DNA.
T + A OR A + T present in the DNA.

Be careful, a CGC sequence is counted only once.
"""

import matplotlib.pyplot as plt

try: # Si le fichier texte existe
     # On ouvre et lit tout le fichier contenant la séquence DNA
    DNA_0 = open("DNAFile.txt").read().strip()
    DNA = DNA_0.replace("\n", "").replace(" ", "")  #On retire les sauts de lignes et les espaces
    # On compte les combinaisons "CG", "GC", en retirant 1 si chevauchements
    cg_count = DNA.count("CG")
    gc_count = DNA.count("GC")
    cgc_chevauché_count = DNA.count("CGC")
    gcg_chevauché_count = DNA.count("GCG")
    total_cg = cg_count + gc_count - cgc_chevauché_count - gcg_chevauché_count
    # On compte les combinaisons "TA" et "AT", en retirant 1 si chevauchements
    at_count = DNA.count("AT")
    ta_count = DNA.count("TA")
    ata_chevauché_count = DNA.count("ATA")
    tat_chevauché_count = DNA.count("TAT")
    total_at = at_count + ta_count - ata_chevauché_count - tat_chevauché_count

    # Calcul du pourcentage par rapport à la longueur totale
    total = len(DNA)
    percent_cg = (2*total_cg / total) * 100 # 1 paire = 2 nucléotides, donc x2
    percent_at = (2*total_at / total) * 100 # 1 paire = 2 nucléotides, donc x2

    print("ADN :", DNA)
    print("Nombre de paires 'C+G' :", total_cg, "->", f"{percent_cg:.2f}%", "des nucléotides appartiennent à la paire C+G.") # On fiche le résultat arrondi à un float avec 2 chiffres après la virgule
    print("Nombre de paires 'A+T' :", total_at, "->", f"{percent_at:.2f}%", "des nucléotides appartiennent à la paire A+T.") # Même chose pour AT

    # matplotlib
    reste = 100 - percent_cg - percent_at
    labels = ["Combinaison C+G", "Combinaison A+T", "Non C+G/A+T"]
    values = [percent_cg, percent_at, reste]

    plt.pie(values, labels=labels, colors=["blue", "red", "gray"], autopct="%.2f%%")
    plt.title("Pourcentage de récurrence des ADN")
    plt.axis("equal") # Avoir un camembert rond
    plt.show()
    
except FileNotFoundError: # Si le fichier texte n'existe pas
    print("Erreur : le fichier 'DNAFile.txt' est introuvable. Vérifie son nom ou son emplacement.")
