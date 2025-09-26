"""
Paul WU 
Bachelor B3 - Développeur IA - ECE

"""

import tkinter as tk
from tkinter import filedialog, messagebox

# Partie 1 : Fonctions pour trier
def is_digit_str(s): # Vérifie si c'est une chaîne de caractère avec seulement des chiffres (Utile après avoir converti le RIB en chiffre)
    if len(s) == 0:
        return False
    for ch in s:
        if not ('0' <= ch <= '9'):
            return False
    return True

def is_digit_or_upper(s):  # Vérifie si c'est une chaîne de caractère avec seulement des chiffres ou des lettres majuscules
    if len(s) == 0:
        return False
    for ch in s:
        if not (('0' <= ch <= '9') or ('A' <= ch <= 'Z')):
            return False
    return True

def strip_spaces(s): # Enlève les espaces, les retours à la ligne, etc
    s = s.upper()
    result = ""
    for ch in s:
        if ch not in (" ", "\n", "\t", "\r"):
            result += ch
    return result

def text_into_tokens(text): # Donne une liste triée avec les mots en majuscule et les chiffres, à partir d'un texte 
    text = text.upper()
    tokens, mot = [], ""  # On construit des mots, qui seront ensuite envoyé dans le token
    for ch in text:
        if ('0' <= ch <= '9') or ('A' <= ch <= 'Z'):
            mot += ch
        else:
            if mot != "":
                tokens.append(mot)
                mot = ""
    if mot != "": 
        tokens.append(mot)
    return tokens

# Partie 2 : Fonctions pour calculer l'IBAN
def cle_iban_fr(bban):
    # convertir BBAN + FR00 en chiffres
    iban_artificiel = bban + "FR00"
    numeric = ""
    for ch in iban_artificiel:
        if '0' <= ch <= '9': 
            numeric += ch
        else:  # Convertir les lettres en chiffres, conformément à la table de conversion
            numeric += str(ord(ch) - 55)
    r = 0
    for ch in numeric:
        r = (r * 10 + (ord(ch) - 48)) % 97 # On calcule le reste de "numeric" par modulo 97
    return f"{98 - r:02d}" # Puis on fait 98 moins le reste pour obtenir la clé de l'iban

def extraire_rib(contenu): # Fonction qui extrait les données utiles d’un RIB
    banque = agence = compte = cle = None

    for l in contenu.splitlines(): # Ligne par ligne, on enlève les espaces 
        l = l.strip()
        if not l: 
            continue # (Bien sûr s'il y en a)

        low = l.lower() 
        parts = l.split() # Ligne par ligne, on sépare et stocks les différents mots
        if not parts:
            continue # (Bien sûr s'il y en a)

        brut = parts[-1] # Et on garde le dernier mot de chaque ligne (car c'est le plus important)
        token = strip_spaces(brut) # stri_spaces remets les mots en majuscules également

        propre = "" # On enlève toute les ponctualités et ne garde que les chiffres et mots
        for ch in token:
            if ('0' <= ch <= '9') or ('A' <= ch <= 'Z'):
                propre += ch
        if propre == "":
            continue

        # Sélection selon libellés
        if ("code" in low) and ("banque" in low):
            # Garder uniquement les chiffres
            digits = ""
            for ch in propre:
                if '0' <= ch <= '9':
                    digits += ch
            if is_digit_str(digits) :
                banque = digits  # 5 chiffres attendus pour le code banque

        elif ("code" in low) and ("agence" in low):
            digits = ""
            for ch in propre:
                if '0' <= ch <= '9':
                    digits += ch
            if is_digit_str(digits) :
                agence = digits  # 5 chiffres attendus pour le code d'agence

        elif ("numéro" in low and "compte" in low) or ("numero" in low and "compte" in low) or ("compte" in low):
            if is_digit_or_upper(propre) and len(propre) == 11:
                compte = propre # 11 chiffres attendus pour le numéro de compte

        elif ("clé" in low) or ("cle" in low) or ("chiffre" in low):
            digits = ""
            for ch in propre:
                if '0' <= ch <= '9':
                    digits += ch
            if is_digit_str(digits) :
                cle = digits  # 2 chiffres attendus pour la clé

    if banque and agence and compte and cle: # Si on obtient les 4 nombres
        return banque, agence, compte, cle
    return None

# Partie 3 : Boutons de l'interface graphique (tkinter)
def ouvrir_fichier_btn(): # Pour le 1er bouton : ouvrir un fichier
    path = filedialog.askopenfilename(
        title="Choisir un fichier RIB",
        filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
    )
    if not path: return
    try:
        with open(path, "r", encoding="utf-8") as f:
            contenu = f.read()
    except Exception as e:
        messagebox.showerror("Erreur", f"Lecture impossible:\n{e}"); return
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, contenu)

def generer_iban_btn(): # Pour le 2eme bouton : générer IBAN
    contenu = text_widget.get("1.0", tk.END).strip() 
    if not contenu: # 1ere erreur : si jamais aucun fichier n'a été séléctionné
        messagebox.showwarning("Avertissement", "Veuillez d'abord, ouvrir un fichier RIB.")
        return
    found = extraire_rib(contenu)
    if not found: # 1ere erreur : si jamais le fichier n'a pas les données requises
        messagebox.showerror("Erreur",
            "Votre RIB ne semble pas être valide.\n"
            "Attendu : banque(5), agence(5), compte(11), clé(2).")
        return

    banque, agence, compte, cle = found # On vérifie désormais la taille des informations requises
    if not (len(banque)==5 and is_digit_str(banque)):  messagebox.showerror("Erreur", f"Code banque invalide : {banque}"); return
    if not (len(agence)==5 and is_digit_str(agence)):  messagebox.showerror("Erreur", f"Code agence invalide : {agence}"); return
    if not (len(compte)==11 and is_digit_or_upper(compte)): messagebox.showerror("Erreur", f"Numéro de compte invalide : {compte}"); return
    if not (len(cle)==2 and is_digit_str(cle)):       messagebox.showerror("Erreur", f"Clé RIB invalide : {cle}"); return

    # construire IBAN en asssemblant tout
    bban = strip_spaces(banque) + strip_spaces(agence) + strip_spaces(compte) + strip_spaces(cle)
    iban = "FR" + cle_iban_fr(bban) + bban
    result_var.set(iban)

# Partie 4 : Visuel de l'interface graphique (tkinter)
root = tk.Tk()
root.title("Convertisseur de RIB en IBAN (en Python)")

text_widget = tk.Text(root, width=60, height=16)
text_widget.pack(padx=10, pady=(10, 6))

frm = tk.Frame(root); frm.pack(pady=4)
tk.Button(frm, text="Ouvrir fichier RIB", command=ouvrir_fichier_btn).grid(row=0, column=0, padx=5)
tk.Button(frm, text="Générer IBAN", command=generer_iban_btn).grid(row=0, column=1, padx=5)

tk.Label(root, text="IBAN obtenu :").pack(anchor="w", padx=10)
result_var = tk.StringVar()
tk.Entry(root, textvariable=result_var, width=60, state="readonly").pack(padx=10, pady=(0, 10))

root.mainloop() 