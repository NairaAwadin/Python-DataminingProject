'''
    lien rendu : https://forms.gle/wNtYYVC1nbacXA7e6

    a faire:
    # ajouter un truc tkinter
    # genere la cle de controle tout seul
    # Accéder au Web Service publique de vérification d'IBAN
    # https://fr.iban.com/validation-api#:~:text=L'API%20de%20validation%20IBAN%20V4%20vous%20permet%20de…

'''
from tkinter import *
from tkinter import filedialog as fd

def open_file(file_name):
    try:
        filename = open(file_name)
        file_content = filename.read() #je stock le contenu du fichier
        filename.close()
        if not file_content.strip(): # ici on verifie si fichier est vide ou s'il contient que des espaces
            print("Le fichier est vide !")
            exit(84)
        return file_content
    except FileNotFoundError:
        print("Fichier non trouvé !")
        exit(84)

def extract_iban(file_content):
    lines = file_content.splitlines()  # pour séparer en lignes
    banque = "" # creation de mes variables vides pour stocker les infos
    agence = ""
    compte = ""
    cle = ""

    for line in lines: #on parcourt chaque ligne
        line = line.strip() # on supprime les espaces au debut et a la fin de la chaine grace a la fonction strip()
        line_lower = line.lower() # ici je convertis toute la chaine en miniscule comme ca je pourrais recuperer les infos meme si c'est ecrit en maj
        if "code banque" in line_lower:
            banque = line.split()[-1] # je decoupe la chaine en utilisant le seperateur espace et l"index -1 c'est parce qu'on veut recuperer le dernier element de la liste et donc les valeurs dans notre cas
        if "code agence" in line_lower:
            agence = line.split()[-1]
        if "numero de compte bancaire" in line_lower:
            compte = line.split()[-1]
        if "chiffre d'indicatif national" in line_lower:
            cle = line.split()[-1]

    if not (banque and agence and compte and cle):
        print("Il manque une information dans votre fichier compte .txt.")
        exit (84)

    return banque, agence, compte, cle

def concatenate_iban(file_content):
    banque, agence, compte, cle = extract_iban(file_content)
    iban_tmp = banque + agence + compte + cle + "152700" # cette fonction concatene les infos du iban et j'ai rajouté la valeur 152700 a la fin pour calculer la clé iban par la suite

    return iban_tmp

def convert_letters(iban_tmp): # comme parfois y'a des lettres parfois dans le numéro de compte bancaire, j'ai crée cette fonction pour reconvertir ces lettres en nombre
    numerique_iban = ""
    for char in iban_tmp:
        if char.isalpha(): # si on trouve une lettre
            value = ord(char.upper()) - 55 # on soustrait - 55 a la valeur ascii de la lettre. EX avec A -> 65 - 55 = 10, et si on se base sur le tableau de conversion A = 10
            numerique_iban = numerique_iban + str(value)
        else:
            numerique_iban = numerique_iban + char
    return numerique_iban

def generate_iban(iban_tmp):
    numerique_iban= convert_letters(iban_tmp)

    reste = int(numerique_iban) % 97 # On calcule le reste de la divison avec 97
    cle_iban = 98 - reste # on soustrait le reste de 98 pour avoir la cle
    if cle_iban < 10:
        cle_iban = "0" + str(cle_iban) # on ajoute un 0 avant si le rest est inférieur a 10
    else:
        cle_iban = str(cle_iban)

    iban_final = "FR" + cle_iban + iban_tmp[:-6]  # on enlève le FR00 déjà ajouté precedemment a la fin
    #print("Cle iban :", cle_iban)
    return iban_final

#content = open_file("bankaccount.txt")
#iban_tmp = concatenate_iban(content)
#iban_final = generate_iban(iban_tmp)
#print("IBAN généré :", iban_final) # le print que j'utilisais avant de coder l'interface graphique avec tkinter

def loading_file_interface():
    file = fd.askopenfilename( # boite de dialogue pour choisir un fichier
        title = "Téléchargez un fichier compte",
        filetypes = [("Text files", "*.txt")])
    if file: #si l'utilisateur selectionne un fichier
        content = open_file(file) # on appelle nos fonctions
        iban_tmp = concatenate_iban(content)
        iban_final = generate_iban(iban_tmp)
        resultat.config(text = "IBAN généré : " + iban_final) # cette ligne affiche le resultat de l'iban dans l'interface

fenetre = Tk() # creation de la fenetre principale
fenetre.title("Générateur d'IBAN")
fenetre.geometry("450x250")

titre = Label(fenetre,
    text = "Générateur d'IBAN",
    font = ("Arial", 18, "bold"), fg = "blue")
titre.pack(pady = 15)

frame_btn = Frame(fenetre)
frame_btn.pack(pady = 10)

btn_fichier = Button(frame_btn,
    text = "Choisir un fichier",
    font = ("Arial", 12),
    bg = "#cce6ff",
    fg = "blue",
    padx = 10,
    pady = 5,
    command = loading_file_interface) # on execute la fonction quand l'utilisateur clique
btn_fichier.pack()

resultat = Label(fenetre, text = "",
    font = ("Arial", 14), fg = "green", justify = "center")
resultat.pack(pady=20)

fenetre.mainloop() # boucle principale : lance l'interface graphique
