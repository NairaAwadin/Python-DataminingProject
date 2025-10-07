'''
    Exercise: Write a program to process a file of DNA text, such as:

    ATGCAATTGCTCGATTAG

    Count the percent of C+G OR G+C present in the DNA. T + A OR A + T present in the DNA.

    Be careful, a CGC sequence is counted only once.

    Faire sortir les statistic via matplot

    https://egallic.fr/Enseignement/Python/visualisation-de-donnees.html

    rendu : https://forms.gle/3CThS1sY4hpKuaQP9
'''
import matplotlib.pyplot as plt

def display_camembert(percent_cg, percent_at):
    my_labels = ["C+G", "A+T"] # liste des noms a afficher sur le graphique
    my_percentages = [percent_cg, percent_at] # liste des valeurs à afficher
    my_colors = ["orange", "blue"]
    plt.pie(my_percentages, labels = my_labels, colors = my_colors) # cette ligne crée le camembert
    plt.title("Pourcentage de C+G et T+A dans l'ADN") # ca c'est pour ajouter le titre au graphique
    plt.show() # ici on l'affiche

def open_file(file_name): # j'ai passé le nm du fichier en parametre
    filename = open(file_name)
    file_content = filename.read() # je stock le contenu du fichier
    filename.close()
    return file_content

def cleaned_file(file_name):
    file_content = open_file(file_name)
    file_content = file_content.replace("\n", "") #enlever les retours a la ligne
    valid_content = "ATCG" # donc ca c'est pour enlever tous les autres charactères apart atcg

    cleaned_sequence = "" # creation d'une chaine vide
    for char in file_content:
        if char in valid_content:
            cleaned_sequence = cleaned_sequence + char #on la remplit avec les char valides

    return cleaned_sequence

def calcul_paires(file_name):
    sequence = cleaned_file(file_name) # on récupère notre chaine de charactère valide

    count_cg = 0 # on initialise nos compteurs
    count_at = 0

    i = 0
    while i < len(sequence):
        if sequence[i:i+3] == "CGC": # donc si on a cgc
            count_cg = count_cg + 1 # on le compte une seule fois
            i = i + 2 # on saute le G pour empecher le double comptage
        else:
            paire = sequence[i:i+2] # parce qu'on veut prendre 2 lettres à chaque itération pour ensuite pouvoir comparer

            if paire == "CG" or paire== "GC":
                count_cg = count_cg + 1

            if paire == "AT" or paire == "TA":
                count_at = count_at + 1

            i = i + 1 # on incremente de 1 pour avancer dans la chaine normalement

    total_paires = count_cg + count_at
    if total_paires > 0:
        percent_cg = (count_cg / total_paires) * 100
        percent_at = (count_at / total_paires) * 100
    else:
        print("Le fichier est vide") #ici on gere l'erreur si jamais on a une divison par 0, ca veut dire que le fichier est vide
        exit (84) # code erreur

    print("Nb paire C+G :", count_cg)
    print("Nb paire A+T :", count_at)
    print("Pourcentage C+G :", round(percent_cg,2), "%") #on utilise round ici pour avoir 2 chiffre apres la virgule
    print("Pourcentage A+T :", round(percent_at,2), "%")

    display_camembert(percent_cg, percent_at)
    return percent_cg, percent_at

calcul_paires("DNAFile.txt")
