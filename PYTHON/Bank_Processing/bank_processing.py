"""
** Python Project : Bank Processing
** Contributors : Leo, Yane, Paul, Mika et Naira
** Date : 19/10/2025
"""

import tkinter as tk
from tkinter import filedialog as fd
import requests

def open_file(file_name):
    try:
        filename = open(file_name)
        file_content = filename.read()
        filename.close()
        if not file_content.strip():
            resultat.config(text="Le fichier est vide !", fg="red")
            return None
        return file_content
    except FileNotFoundError:
        resultat.config(text="Fichier non trouvé !", fg="red")
        return None

def extract_iban(file_content):
    lines = file_content.splitlines()
    banque = agence = compte = cle = ""
    mots_interdits = {"national", "rib", "bancaire", "compte", "indicatif"}
    for line in lines:
        line = line.strip()
        line_lower = line.lower()
        dernier_mot = line.split()[-1].lower()
        if dernier_mot in mots_interdits:
            continue  # ignore la ligne s'il n y a pas de valeur a extraire
        if "code banque" in line_lower:
            banque = line.split()[-1] # decoupe la chaine en utilisant le seperateur espace et l"index -1 c'est parce qu'on veut recuperer le dernier element de la liste et donc les valeurs dans notre cas
        if "code agence" in line_lower:
            agence = line.split()[-1]
        if "numero de compte" in line_lower:
            compte = line.split()[-1]
        if "chiffre d'indicatif" in line_lower or "cle rib" in line_lower:
            cle = line.split()[-1]
    return banque, agence, compte, cle

def charger_fichier():
    file = fd.askopenfilename(
        title="Choisir un fichier compte",
        filetypes=[("Text files", "*.txt")]) # ouvre la boite de dialogue pour select un fichier
    if file:
        content = open_file(file)
        if not content:
            return
        banque, agence, compte, cle = extract_iban(content)
        if not all([banque, agence, compte, cle]):
            resultat.config(text="Informations manquantes dans le fichier", fg="red")
            return
        # remplissage automatique des champs
        entree_banque.delete(0, tk.END)
        entree_agence.delete(0, tk.END)
        entree_compte.delete(0, tk.END)
        entree_cle.delete(0, tk.END)
        entree_banque.insert(0, banque)
        entree_agence.insert(0, agence)
        entree_compte.insert(0, compte)
        entree_cle.insert(0, cle)
        resultat.config(text="Fichier chargé avec succès ✔️", fg="green")

def lettre_to_chiffre(c):
    if c.isdigit():
        return c
    else:
        return str(ord(c.upper()) - 55)

def calculer_cle(banque, agence, compte, cle_rib):
    base = banque + agence + compte + cle_rib + "FR00"
    chiffres = "".join(lettre_to_chiffre(c) for c in base) # convertit chaque char en chiffre et les concatène
    reste = 0
    for i in range(0, len(chiffres), 9): # calcule le reste modulo 97 par blocs de 9 chiffres
        bloc = str(reste) + chiffres[i:i+9]
        reste = int(bloc) % 97
    return str(98 - reste).zfill(2) # calcule la clé RIB finale : 98 moins le reste modulo 97, puis formate le résultat sur 2 chiffres (ex : '07' au lieu de '7')

def generer_iban():
    banque = entree_banque.get().strip()
    agence = entree_agence.get().strip()
    compte = entree_compte.get().strip()
    cle = entree_cle.get().strip()

    if not (banque and agence and compte and cle): # verifie que tous les champs sont remplis
        resultat.config(text="Champs manquants", fg="red")
        return

    if mode.get() == "fixe":
        cle_iban = "14"
    else:
        cle_iban = calculer_cle(banque, agence, compte, cle)

    iban = f"FR{cle_iban}{banque}{agence}{compte}{cle}"

    # affiche l'IBAN généré dans l'interface
    entree_resultat.delete(0, tk.END)
    entree_resultat.insert(0, iban)
    resultat.config(text="✔️ IBAN généré avec succès", fg="green")

def verifier_api():
    iban = entree_resultat.get().strip().replace(" ", "") # on recupere l'iban et on supprime les esp en +
    if not iban:
        resultat.config(text="Aucun IBAN généré à vérifier", fg="red")
        return
    url = f"https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true" # prépare l'url OpenIban pour la validation
    try:
        response = requests.get(url, timeout=8) # envoie requete GET à l'API
        if response.status_code == 200:
            data = response.json()
            if data.get("valid", False): # verif si l'iban est valide
                resultat.config(text="✔️ IBAN valide", fg="green")
            else:
                resultat.config(text="❌ IBAN invalide", fg="red")
        else:
            resultat.config(text=f"Erreur API : {response.status_code}", fg="red")
    except Exception as e:
        resultat.config(text=f"Erreur : {e}", fg="red")

# Interface graphique

fen = tk.Tk()
fen.title("Générateur et Vérificateur IBAN") # titre de la fenêtre
fen.geometry("420x550")

tk.Label(fen,
    text="Générateur et Vérificateur IBAN", # titre affiché dans la fenêtre
    font=("Arial", 16, "bold"),
    fg="navy").pack(pady=10)

btn_charger = tk.Button(fen,
    text="Charger un fichier compte (.txt)", # btn pour charger un fichier
    command=charger_fichier,
    bg="lightblue",
    fg="navy")
btn_charger.pack(pady=8)

tk.Label(fen, text="Code banque").pack() # champs ou les infos sont affichés, peuvent être saisies également
entree_banque = tk.Entry(fen)
entree_banque.pack()

tk.Label(fen, text="Code agence").pack()
entree_agence = tk.Entry(fen)
entree_agence.pack()

tk.Label(fen, text="Numéro de compte").pack()
entree_compte = tk.Entry(fen)
entree_compte.pack()

tk.Label(fen, text="Chiffre d'indicatif national").pack()
entree_cle = tk.Entry(fen)
entree_cle.pack()

mode = tk.StringVar(value="fixe") # variable qui stock le choix selectionné
tk.Radiobutton(fen, text="Clé fixe (14)", variable=mode, value="fixe").pack()
tk.Radiobutton(fen, text="Clé dynamique (calculée)", variable=mode, value="dynamique").pack() # quand l'utilisateur clique sur un btn, la valeur de mode change

btn_generer = tk.Button(fen, text="Générer", command=generer_iban, bg="palegreen")
btn_generer.pack(pady=10)

tk.Label(fen, text="IBAN généré").pack()
entree_resultat = tk.Entry(fen, width=40, justify="center", fg="navy", font=("Arial", 10, "bold"))
entree_resultat.pack(pady=5)

btn_verifier = tk.Button(fen, text="🔎 Vérifier IBAN", command=verifier_api, bg="thistle")
btn_verifier.pack(pady=10)

resultat = tk.Label(fen, text="", font=("Arial", 12)) # label pour afficher les messages de resultat ou d'erreur
resultat.pack(pady=10)

fen.mainloop()