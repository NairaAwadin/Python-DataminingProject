# K-Means (K-Moyennes), avec k = 3 et 14 points

import random
import numpy as np
import matplotlib.pyplot as plt

GRAINE_RANDOM = random.randint(1, 50)
SEED = GRAINE_RANDOM
K = 3
MAX_ITER = 60
TOL = 1e-3
PAUSE = 1.5

random.seed(SEED)
rng = np.random.default_rng(SEED)

# --- Données (14 points uniformes dans [0,10]x[0,10]) ---
X = rng.uniform(low=0, high=10, size=(14, 2))  # shape (14, 2)
n = X.shape[0]  # 14

# --- Init centroïdes = 3 points tirés au hasard (reproductible) ---
init_idx = random.sample(range(n), K)
centroids = X[init_idx].copy()

# ---------- Utilitaires ----------
def pairwise_distances(a, b):
    diff = a[:, None, :] - b[None, :, :]
    return np.sqrt(np.sum(diff**2, axis=2))

def compute_sse(X, centroids, labels):
    diffs = X - centroids[labels]
    return float(np.sum(np.sum(diffs**2, axis=1)))

def reinit_empty_clusters(X, old_centroids, labels, centroids):
    # Réinit d’un cluster vide au point le plus éloigné de son ancien centroïde
    for k in range(K):
        if np.sum(labels == k) == 0:
            d = np.linalg.norm(X - old_centroids[k], axis=1)
            centroids[k] = X[int(np.argmax(d))]
    return centroids

def update_centroids_incremental(X, labels, centroids):
    """
    Recalcule chaque centroïde par moyenne incrémentale :
      mu <- mu + (1/n)(x - mu)
    Ordre déterministe: on parcourt les points dans l’ordre de leur index.
    Si un cluster n’a qu’un seul point, son mu devient ce point (cohérent).
    """
    new_centroids = centroids.copy()
    counts = np.zeros(K, dtype=int)

    # Initialiser à 0: on posera mu = premier x rencontré, puis on incrémentera
    for k in range(K):
        new_centroids[k] = 0.0

    for i in range(n):               # ordre stable (1..14)
        k = labels[i]
        x = X[i]
        counts[k] += 1
        if counts[k] == 1:
            # premier élément du cluster: mu = x
            new_centroids[k] = x
        else:
            # mu <- mu + (1/n)(x - mu)
            mu = new_centroids[k]
            c = counts[k]
            new_centroids[k] = mu + (x - mu) / c

    # Pour les clusters vides, on laisse tel quel; ils seront ré-initialisés après
    return new_centroids, counts

def plot_iteration(iter_idx, X, labels, centroids, old_centroids, sse_value):
    plt.cla()
    colors = ['tab:blue', 'tab:orange', 'tab:green']
    for k in range(K):
        pts = X[labels == k]
        if len(pts) > 0:
            plt.scatter(pts[:, 0], pts[:, 1], s=60, marker='o',
                        color=colors[k], alpha=0.85, label=f'Cluster {k}')
    for i, (x, y) in enumerate(X, start=1):
        plt.text(x + 0.03, y + 0.03, str(i), fontsize=9)

    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='X', s=220, c='k', edgecolors='white',
                linewidths=1.6, label='Centroïdes')

    if old_centroids is not None:
        for k in range(K):
            s, e = old_centroids[k], centroids[k]
            if np.linalg.norm(e - s) > 0:
                plt.annotate('', xy=e, xytext=s,
                             arrowprops=dict(arrowstyle='->', lw=1.6))

    plt.title(f"Itération {iter_idx + 1}  •  SSE = {sse_value:.3f}")
    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.3)

    # 🔥 Axes fixés de 0 à 10
    plt.xlim(0, 10)
    plt.ylim(0, 10)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.pause(PAUSE)

# ---------- Boucle K-Means ----------
plt.figure(figsize=(7, 6))
plt.ion(); plt.show(block=False)

prev_labels = None
for it in range(MAX_ITER):
    old_centroids = centroids.copy()

    # Assignation
    D = pairwise_distances(X, centroids)
    labels = np.argmin(D, axis=1)

    # Mise à jour incrémentale (formule de l’image)
    centroids, counts = update_centroids_incremental(X, labels, centroids)

    # Clusters vides -> réinit intelligente + réassignation
    centroids = reinit_empty_clusters(X, old_centroids, labels, centroids)
    D = pairwise_distances(X, centroids)
    labels = np.argmin(D, axis=1)

    # Mouvement + SSE
    movement = float(np.sum(np.linalg.norm(centroids - old_centroids, axis=1)))
    sse_value = compute_sse(X, centroids, labels)

    # Affichage
    plot_iteration(it, X, labels, centroids, old_centroids, sse_value)

    # Arrêt si labels stables et mouvement faible
    labels_stable = (prev_labels is not None) and np.array_equal(labels, prev_labels)
    if labels_stable and (movement < TOL):
        break
    prev_labels = labels.copy()

plt.ioff(); plt.show()