"""
** Datamining Project : K-Means Algorithm
** Dataset : Line 20, à ajouter dans le code
** Description : Ce programme démontre le principe du K-Means graphiquement 
** Contributors : Leo, Yane, Paul, Mika et Naira
** Date : 19/10/2025
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Button

# Fonction qui calcule la distance euclidienne entre deux points dans un espace n-dimensionnel
def calculate_distance(ptA, ptB):
    """ 
    --> Paramètres : Deux points "A" et "B" 
    --> Retour : Float (distance d'Euclide)
    --> Note : Vérifie en entrée la dimension des 2 points (s'ils ont la même dimension)
    """
    # Converti les points en tableau NumPy pour améliorer les performances & la rapidité du code
    ptA = np.array(ptA, dtype=float)
    ptB = np.array(ptB, dtype=float)
    # Vérifie la dimension
    if ptA.shape != ptB.shape:
        raise ValueError("Points must have the same dimension.")
    # Calcule de la distance Euclidienne
    diff = ptA - ptB                    # Différence sur chaque coordonnée
    squared = diff ** 2                 # Mise au carré de chaque différence
    distance = np.sqrt(np.sum(squared)) # Racine carrée de la somme des carrés
    return distance

# Fonction qui classifie chaque point non classé à son point classé le plus proche, selon la distance euclidienne (plus courte distance).
def get_shortestDistancePairs(classified_pts: list[tuple],
                              unclassified_pts: list[tuple],
                              classify_classified: bool = False):
    """
    --> Paramètres : classified_pts (Points déjà classifiés), 
                     unclassified_pts (Points à classer), 
                     classify_classified (Booléen, si un point est classé ou pas encore) 
    --> Retour : {clés : points, valeurs : classified points}
    --> Note : Tranche avec une comparaison lexicographique* (Si un point a 2 "plus proche voisin" équidistant, on choisit la valeur la plus petite)
    """
    pairs = {}  # Dictionnaire final qui sera retourné à la fin
    # Parcourt chaque point non classé
    for uc_pt in unclassified_pts:
        shortest_distance = float("inf")  # On initie shortest_distance et nearest_neighbour
        nearest_neighbour = None
        # Compare avec chaque point classé
        for c_pt in classified_pts:
            distance = calculate_distance(uc_pt, c_pt)
            # Si une distance plus courte est trouvée
            if distance < shortest_distance:
                shortest_distance = distance  # Mise à jour du shortest_distance avec la nouvelle valeur trouvée
                nearest_neighbour = c_pt      # Mise à jour de son voisin le plus proche (ou centroïde le plus proche)
            # Si distances égales avec 2 centroïdes --> tie-break lexicographique
            elif math.isclose(distance, shortest_distance, abs_tol = CONVERGE): # math.isclose = si 2 valeurs sont très proches 
                nearest_neighbour = min(nearest_neighbour, c_pt)                # Utilisation de la comparaison lexicographique*
        # Ajoute la correspondance dans le dictionnaire
        pairs[uc_pt] = nearest_neighbour
        # Si on veut classifier les centroïdes avec eux-même.
    if classify_classified:
        for c_pt in classified_pts:
            pairs[c_pt] = c_pt
    return pairs

# Fonction qui calcule le centroïde (la moyenne des coordonnées de chaque point, dimension par dimension)
def get_centroid(points : list = None):
    """
    --> Paramètres : Liste de points
    --> Retour : Tuple avec les coordonnées du centroïde
    --> Note : Vérifie que la liste n'est pas vide et que tous les points ont la même dimension 
    """
    # Vérifie que la liste de points n'est pas vide
    if not points :
        return None
    else : 
        # Prend le nombre de dimensions du premier point
        generalized_num_dims = len(points[0])
        if any(len(point) != generalized_num_dims for point in points): # Vérifie si les points ont la même dimension avec le 1er point
            raise ValueError("points inconsitent dimensions")

    return tuple(
        sum(coords) / len(points) # Moyenne de chaque dimension
        for coords in zip(*points)  # Transpose les points pour calculer la moyenne de chaque dimension x, y, ...
    ) # Retourne le résultat sous forme de (moyenne de x, moyenne de y, ...)

# Fonction qui calcule l'inertie (d'un groupe de points avec son centroïde) 
def get_inertia(centroids : list = None, points : list = None):
    """
    --> Paramètres : Liste des centroïdes et la liste de points
    --> Retour : Float avec l'inertie calculé 
    --> Note : Vérifie qu'il y a des points et des centroïdes
    """
    # Vérifie que la liste de points & centroïdes ne sont pas vide
    if not points or not centroids:
        raise ValueError("No centroids or points given")
    # Converti les données en tuple, pour pouvoir utiliser la fonction get_shortestDistancePairs     
    cents_t  = [tuple(c) for c in centroids]
    points_t = [tuple(p) for p in points]
    # Récupère, pour chaque point, le centroïde le plus proche
    pairs = get_shortestDistancePairs(
        classified_pts=cents_t,
        unclassified_pts=points_t,
        classify_classified=False
    )
    # Calcule l'inertie (Formule = somme de chaque distance euclienne de chaque points avec son centroïde au carré)
    inertia = 0.0
    for p in points_t: # Parcours chaque points
        c = pairs[p]   # Extrait son centroïde
        d = calculate_distance(p, c) # Calcule sa distance euclidienne
        inertia += d * d # Application de la formule de l'inertie
    return float(inertia)

#  Fonction qui attribue à chaque point un label (numéro de cluster)
def labels_from_pairs(X, centroids):
    """
    --> Paramètres : Liste des centroïdes et la liste des points du dataset
    --> Retour : Tableau NumPy de labels de clusters  
    """
    # Converti les données en tuple, pour pouvoir utiliser la fonction get_shortestDistancePairs
    pts_t = [tuple(p) for p in X]
    cts_t = [tuple(c) for c in centroids]
    pairs = get_shortestDistancePairs(cts_t, pts_t) # On défini le centroïde le plus proche de chaque point
    idx = {c: i for i, c in enumerate(cts_t)} # Remplace le centroïde associé à chaque point par son index numérique
    return np.array([idx[pairs[pt]] for pt in pts_t], dtype=int)

# Fonction qui réalise 1 itération de l'Algorithme de Lloyd / K-Means
def kmeans_one_iteration(X, centroids):
    """
    --> Paramètres : Liste des centroïdes et la liste des points du dataset
    --> Retour : Labels/clusters de chaque points, les nouveaux centroïdes et la valeur de l'inertie 
    --> Note : 
        1. Attribue chaque point à son centroïde le plus proche (avec "labels_from_pairs")
        2. Recalcule le centroïde de chaque cluster (avec "get_centroid")
        3. Calcule l'inertie globale du regroupement (avec "get_inertia")
    """
    labels = labels_from_pairs(X, centroids) # Récupération des labels avec "labels_from_pairs"
    new_centroids = []
    for k in range(len(centroids)): # Parcours chaque cluster
        pts_k = X[labels == k]      # Range par cluster chaque points du dataset
        if len(pts_k) > 0:
            c = get_centroid([tuple(p) for p in pts_k])    # Calcule le centroïde d'un cluster à partir de ses points
            new_centroids.append(np.array(c, dtype=float)) # Stocke le centroïde dans la liste "new_centroids"
        else:
            new_centroids.append(centroids[k].copy()) # Si jamais le cluster est vide --> on le conserve
    new_centroids = np.vstack(new_centroids)
    # Récupération de l'inertie avec "get_inertia"
    inertia = float(get_inertia(
        centroids=[tuple(c) for c in new_centroids],
        points=[tuple(p) for p in X]
    ))
    return labels, new_centroids, inertia

# Fonction qui illustre graphiquement le processus du K-Means
def plot_iteration(iter_idx, X, labels, centroids, old_centroids, inertia_value):
    ax_main.cla() # Initiation d'un nouveau graphique (efface l'ancien)
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
              'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
    K_local = centroids.shape[0]
    # Affichage des points du dataset
    for k in range(K_local):
        pts = X[labels == k]
        if len(pts) > 0:
            ax_main.scatter(pts[:, 0], pts[:, 1], s=60, marker='o',
                            color=colors[k % len(colors)], alpha=0.85, label=f'Cluster {k}')
    # Affichage des indices de chaque points
    for i, (x, y) in enumerate(X, start=1):
        ax_main.text(x + 0.03, y + 0.03, str(i), fontsize=9)
    # Affichage des centroïdes
    ax_main.scatter(centroids[:, 0], centroids[:, 1],
                    marker='X', s=100, c='k', edgecolors='white',
                    linewidths=1.6, label='Centroïdes')
    # Affichage des flèches (mouvement des centroïdes)
    if old_centroids is not None:
        for k in range(K_local):
            s, e = old_centroids[k], centroids[k]
            if np.linalg.norm(e - s) > 0:
                ax_main.annotate('', xy=e, xytext=s,
                                 arrowprops=dict(arrowstyle='->', lw=1.6))
    # Paramètre du titre, de la légende et du grillage en fond
    ax_main.set_title(f"Itération n°{iter_idx}  /  Valeur de l'inertie = {inertia_value:.3f}", pad=10)
    ax_main.legend(loc='best')
    ax_main.grid(True, linestyle='--', alpha=0.3)
    # Paramètre du cadrage auto avec marge
    pad = 1.0
    ax_main.set_xlim(X[:,0].min()-pad, X[:,0].max()+pad)
    ax_main.set_ylim(X[:,1].min()-pad, X[:,1].max()+pad)
    ax_main.set_aspect('equal', adjustable='box')
    fig.canvas.draw_idle() # Permet à l'utilisation du bouton "Next"

# Fonction run (lance l'itération n°0)
def init_run():
    # Réinitialisation des paramètres de l'état global
    state["iter"] = 0
    state["prev_labels"] = None
    state["converged"] = False
    # Sélection aléatoire des centroïdes
    idx = rng.choice(len(X), size=K, replace=False)
    state["centroids"] = X[idx].copy()
    # Attribution des points aux centroïdes initiaux
    labels = labels_from_pairs(X, state["centroids"])
    # Calcul de l'inertie initiale
    inertia0 = float(get_inertia(
        centroids=[tuple(c) for c in state["centroids"]],
        points=[tuple(p) for p in X]
    ))
    # Enregistrement des labels et de l'inertie, puis affichage de l’itération 0
    state["labels"], state["inertia"] = labels, inertia0
    plot_iteration(state["iter"], X, state["labels"], state["centroids"], None, state["inertia"])

# Fonction qui relance "init_run" à partir de 0
def on_reset(event):
    init_run()

# Fonction qui exécute une itération supplémentaire de l'algorithme K-Means
def on_next(event):
    # Vérifie si la fonction ne peut plus être itéré ou pas 
    if state["converged"] or state["iter"] >= MAX_ITER:
        return
    oldC = state["centroids"].copy()                                    # Sauvegarde des centroïdes actuels
    labels, Cnew, inertia = kmeans_one_iteration(X, state["centroids"]) # Effectue une itération du K-Means
    movement = float(np.sum(np.linalg.norm(Cnew - oldC, axis=1)))       # Calcule le déplacement total des centroïdes entre deux itérations
    # Mise à jour des variables d'état global après le "click"
    state["iter"] += 1
    state["prev_labels"] = state["labels"]
    state["labels"], state["centroids"], state["inertia"] = labels, Cnew, inertia
    # Mise à jour du graphique également
    plot_iteration(state["iter"], X, state["labels"], state["centroids"], oldC, state["inertia"])
    # Vérifie si les centroïdes sont stables et si elles ne convergent pas
    labels_stable = (state["prev_labels"] is not None) and np.array_equal(state["labels"], state["prev_labels"])
    if (labels_stable and movement < CONVERGE) or (state["iter"] >= MAX_ITER):
        state["converged"] = True

# ----------------------------------------------------------------------- #

# Paramètres d'initialisation
K = 3 # Nombre de centroïdes
MAX_ITER = 100 # Nombre d'itération maximal
CONVERGE = 1e-6 # Seuil minimal de mouvement des centroïdes, sinon on considérera que la fonction a convergé

#  Initiation du Dataset
X = np.array([
    (1.0, 1.4), (3.3, 2.1), (0.8, 3.2), (7.2, 4.7), (5.5, 5.9),
    (8.2, 6.3), (2.5, 7.9), (2.8, 8.1), (6.0, 1.6), (7.3, 2.7),
    (2.2, 3.6), (3.5, 4.1), (5.9, 0.4), (4.3, 6.8), (7.0, 7.9)
], dtype=float)

#  État global de l'algorithme K-Means
state = {
    "iter": 0,
    "centroids": None,
    "labels": None,
    "inertia": None,
    "prev_labels": None,
    "converged": False,
}

 # Initiation de la graine
rng = np.random.default_rng(42)

# Figure Matplotlib + zones pour les boutons
plt.close("all")
fig = plt.figure(figsize=(7.5, 6.5))
# Axe principal pour le graphique
ax_main = fig.add_axes([0.10, 0.16, 0.86, 0.78])
# Axes pour les boutons
ax_reset = fig.add_axes([0.20, 0.04, 0.15, 0.07])
ax_next  = fig.add_axes([0.38, 0.04, 0.20, 0.07])

# Boutons
btn_reset = Button(ax_reset, "Reset")
btn_next  = Button(ax_next,  "Next (itération)")
btn_reset.on_clicked(on_reset)
btn_next.on_clicked(on_next)

# Lancement
init_run()
plt.show()