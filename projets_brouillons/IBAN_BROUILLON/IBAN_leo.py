import tkinter as tk 
import requests  # pour l'API de vérification

# conversion lettre en chiffre (A=10, B=11, ...)
def lettre_to_chiffre(c):
    if c.isdigit():
        return c
    else:
        return str(ord(c.upper()) - 55)

# calcule la clé de contrôle IBAN (mod 97) pour une BBAN française
def calculer_cle(banque, agence, compte, cle_rib):
    base = banque + agence + compte + cle_rib + "FR00"
    chiffres = "".join(lettre_to_chiffre(c) for c in base)

    reste = 0
    for i in range(0, len(chiffres), 9):
        bloc = str(reste) + chiffres[i:i+9]
        reste = int(bloc) % 97

    return str(98 - reste).zfill(2)

# génère l'IBAN FR à partir des champs (clé fixe = 14)
def generer():
    banque = entree_banque.get().strip()
    agence = entree_agence.get().strip()
    compte = entree_compte.get().strip()
    cle = entree_cle.get().strip()

    if not (banque and agence and compte and cle):
        resultat.config(text="Champs manquants")
        return

    if mode.get() == "fixe":
        cle_iban = "14"
    else:
        cle_iban = calculer_cle(banque, agence, compte, cle)

    iban = f"FR{cle_iban}{banque}{agence}{compte}{cle}"
    resultat.config(text="IBAN : " + iban)

# vérifie l'IBAN via l'API OpenIBAN 
def verifier_api():
    iban = entree_verif.get().strip().replace(" ", "")
    if not iban:
        resultat.config(text="Veuillez entrer un IBAN à vérifier")
        return

    url = f"https://openiban.com/validate/{iban}?getBIC=true&validateBankCode=true"
    try:
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            if data.get("valid", False):
                resultat.config(text="IBAN valide")
            else:
                resultat.config(text="IBAN invalide")
        else:
            # Si erreur  API 
            resultat.config(text=f"Erreur API : {response.status_code}")
    except Exception as e:
        # problème autre
        resultat.config(text=f"Erreur : {e}")

# --- Interface Tkinter ---
fen = tk.Tk()
fen.title("Générateur et Vérificateur IBAN")
fen.geometry("400x500")

# champs pour générer un IBAN
tk.Label(fen, text="Code banque").pack()
entree_banque = tk.Entry(fen)
entree_banque.pack()

tk.Label(fen, text="Code agence").pack()
entree_agence = tk.Entry(fen)
entree_agence.pack()

tk.Label(fen, text="Numéro de compte").pack()
entree_compte = tk.Entry(fen)
entree_compte.pack()

tk.Label(fen, text="Clé RIB").pack()
entree_cle = tk.Entry(fen)
entree_cle.pack()

# choix mode : fixe (14) ou dynamique (calculée)
mode = tk.StringVar(value="fixe")
tk.Radiobutton(fen, text="Clé fixe (14)", variable=mode, value="fixe").pack()
tk.Radiobutton(fen, text="Clé dynamique (calculée)", variable=mode, value="dynamique").pack()

tk.Button(fen, text="Générer", command=generer).pack(pady=10)

# zone pour vérifier un IBAN  via API
tk.Label(fen, text="Entrer un IBAN à vérifier").pack(pady=5)
entree_verif = tk.Entry(fen, width=40)
entree_verif.pack()
tk.Button(fen, text="Vérifier (API OpenIBAN)", command=verifier_api).pack(pady=10)

# Confirmation IBAN valide ou invalide
resultat = tk.Label(fen, text="", font=("Arial", 12))
resultat.pack(pady=10)

fen.mainloop()
