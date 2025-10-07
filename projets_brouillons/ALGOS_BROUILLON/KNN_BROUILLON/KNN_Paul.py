# K-NN (K-Nearest Neighbors / K-Plus Proches Voisins), avec k = 1 et 14 points

import numpy as np
import matplotlib.pyplot as plt
import random


# -----------------------------
# Paramètres généraux
# -----------------------------
GRAINE_RANDOM = random.randrange(1, 50)
N = 14
SEED = GRAINE_RANDOM
BOX_X = (0.0, 10.0)  # domaine d'échantillonnage
BOX_Y = (0.0, 6.0)

rng = np.random.default_rng(SEED)

# -----------------------------
# 1) Génération des points
# -----------------------------
X = np.empty((N, 2), dtype=float)
X[:, 0] = rng.uniform(*BOX_X, size=N)
X[:, 1] = rng.uniform(*BOX_Y, size=N)

# -----------------------------
# 2) Graines: 2 rouges, 2 bleues
# -----------------------------
labels = -np.ones(N, dtype=int)   # -1 = non étiqueté, 0 = rouge, 1 = bleu
seed_idx = rng.choice(N, size=4, replace=False)
red_idx  = seed_idx[:2]
blue_idx = seed_idx[2:]

labels[red_idx]  = 0
labels[blue_idx] = 1

# -----------------------------
# 3) Outils d'affichage
# -----------------------------
def label_to_color(lbl):
    if lbl == 0:  # rouge
        return 'tab:red'
    if lbl == 1:  # bleu
        return 'tab:blue'
    return 'lightgray'  # non étiqueté

def draw(ax, step_title=""):
    ax.clear()
    colors = [label_to_color(l) for l in labels]
    sizes  = np.full(N, 60)
    sizes[labels == -1] = 40            # non étiquetés un peu plus petits
    sizes[(labels != -1) & np.isin(np.arange(N), seed_idx)] = 90  # graines plus grandes

    ax.scatter(X[:, 0], X[:, 1], c=colors, s=sizes, edgecolor='k', zorder=2)
    # Numéroter les points (1..14)
    for i, (x, y) in enumerate(X):
        ax.text(x + 0.06, y + 0.06, str(i + 1), fontsize=9, zorder=3)

    ax.set_xlim(BOX_X); ax.set_ylim(BOX_Y)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title(step_title)
    ax.grid(alpha=0.3)

# -----------------------------
# 4) Propagation 1-NN
# -----------------------------
log_steps = []

fig, ax = plt.subplots(figsize=(7, 4))
plt.ion()
draw(ax, "Étape 0 — Graines (2 rouges, 2 bleues)")
plt.pause(0.8)

step = 0
while np.any(labels == -1):
    labeled_idx   = np.where(labels != -1)[0]
    unlabeled_idx = np.where(labels == -1)[0]

    # Distances de chaque non-etiq vers chaque étiqueté
    A = X[unlabeled_idx][:, None, :] - X[labeled_idx][None, :, :]
    dists = np.linalg.norm(A, axis=2)  # shape (U, L)

    # Trouver le couple (u, l) de distance minimale
    flat = np.argmin(dists)
    u_pos, l_pos = np.unravel_index(flat, dists.shape)
    u_idx = unlabeled_idx[u_pos]
    l_idx = labeled_idx[l_pos]
    dmin  = dists[u_pos, l_pos]

    # 1-NN: prendre l'étiquette du plus proche voisin étiqueté
    labels[u_idx] = labels[l_idx]
    color_name = "rouge" if labels[u_idx] == 0 else "bleu"
    step += 1
    log_steps.append(f"Étape {step}: le point {u_idx + 1} devient {color_name} (d = {dmin:.3f})")

    # Affichage incrémental
    draw(ax, f"Étape {step} — point {u_idx + 1} -> {color_name}")
    # Optionnel: montrer l'arête la plus proche
    ax.plot([X[u_idx, 0], X[l_idx, 0]], [X[u_idx, 1], X[l_idx, 1]], '--', alpha=0.4, zorder=1)
    plt.pause(0.6)

plt.ioff()
draw(ax, "Terminé — tous les points sont colorés")
plt.show()

# -----------------------------
# 5) Récapitulatif console
# -----------------------------
print("\nRÉCAPITULATIF DES ÉTAPES (1-NN):")
for line in log_steps:
    print(line)
