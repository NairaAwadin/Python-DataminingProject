import tkinter as tk
from tkinter import filedialog, messagebox

# Fonction qui ouvre un fichier ADN et analyse la séquence
def ouvrir_traiter_fichier(zone_texte):
    chemin = filedialog.askopenfilename(
        title="Choisir un fichier ADN",
        filetypes=[("Fichiers texte", "*.txt")]
    )
    
    if not chemin:
        # Aucun fichier choisi
        return None  
    
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier :\n{e}")
        return None

    # Rendre la zone éditable pour insérer le texte
    zone_texte.config(state=tk.NORMAL)
    zone_texte.delete("1.0", tk.END)
    zone_texte.insert(tk.END, contenu)

    # Préparer la séquence ADN
    my_dna = contenu.strip().upper()
    
    # Compter les paires CG/GC et AT/TA
    i = 0
    cg_count = 0
    at_count = 0
    while i < len(my_dna) - 1:
        pair = my_dna[i:i+2]
        if pair in ("CG", "GC"):
            cg_count += 1
            i += 2
            # Retour à la vérif de la condition
            continue
        elif pair in ("AT", "TA"):
            at_count += 1
            i += 2
            continue
        # Si ni CG/GC ou AT/TA, on avance paire suivante
        i += 1

    total_pairs = cg_count + at_count
    percent_cg = (cg_count / total_pairs) * 100 if total_pairs > 0 else 0
    percent_at = (at_count / total_pairs) * 100 if total_pairs > 0 else 0

    # Afficher les résultats à la fin de la zone de texte
    zone_texte.insert(tk.END, "\n\n--- Analyse ADN ---\n")
    zone_texte.insert(tk.END, f"Paires CG/GC : {cg_count}\n")
    zone_texte.insert(tk.END, f"Paires AT/TA : {at_count}\n")
    zone_texte.insert(tk.END, f"% CG/GC : {percent_cg:.2f}%\n")
    zone_texte.insert(tk.END, f"% AT/TA : {percent_at:.2f}%\n")

    # Bloquer la modif de la zone de texte
    zone_texte.config(state=tk.DISABLED)
    
    return my_dna

# Fenêtre principale tkinter
fenetre = tk.Tk()
fenetre.title("Analyse ADN")
fenetre.geometry("600x400")

# Zone de texte
zone_texte = tk.Text(fenetre, wrap="word", width=70, height=20)
zone_texte.pack(padx=10, pady=10)

# Bouton pour l'ouverture et l'analyse de mon fichier
bouton = tk.Button(fenetre, text="Ouvrir et analyser ADN", 
                   command=lambda: ouvrir_traiter_fichier(zone_texte))
bouton.pack(pady=10)


fenetre.mainloop()
