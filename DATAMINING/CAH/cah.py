import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

# Configuration
np.random.seed(40)
N_POINTS = 20
X = np.random.rand(N_POINTS, 2) * 10

def dist_euclidienne(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def dist_clusters(c1_indices, c2_indices):
    # Distance inter-clusters par la méthode du Centroid
    pts1, pts2 = X[c1_indices], X[c2_indices]
    c1_mean, c2_mean = np.mean(pts1, axis=0), np.mean(pts2, axis=0)
    return dist_euclidienne(c1_mean, c2_mean)

# Initialisation
clusters = {i: [i] for i in range(N_POINTS)}
merges = []
current_id = N_POINTS

# Algorithme de Classification Hiérarchique Ascendante 
while len(clusters) > 1:
    min_dist = float('inf')
    to_merge = None
    ids = list(clusters.keys())
    
    # Recherche de la paire de clusters la plus proche
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            c1_id, c2_id = ids[i], ids[j]
            d = dist_clusters(clusters[c1_id], clusters[c2_id])
            
            if d < min_dist:
                min_dist = d
                to_merge = (c1_id, c2_id)

    # Enregistrement de la fusion (format SciPy)
    c1, c2 = to_merge
    merges.append([c1, c2, min_dist, len(clusters[c1]) + len(clusters[c2])])

    # Fusion des clusters
    new_cluster_indices = clusters[c1] + clusters[c2]
    clusters[current_id] = new_cluster_indices
    del clusters[c1]
    del clusters[c2]

    current_id += 1

# Matrice d'agrégation Z
Z = np.array(merges)

# Détermination du Seuil pour n_clusters
n_clusters = 3
cut_index = N_POINTS - n_clusters
color_threshold = Z[cut_index, 2]
color_threshold_adjusted = color_threshold * 0.9

def get_cluster_labels_v2(merges_matrix, num_clusters, total_points):
    # Extrait les labels en s'arrêtant lorsque 'num_clusters' est atteint
    cluster_to_points = {i: {i} for i in range(total_points)}
    point_to_cluster_id = list(range(total_points))
    current_cluster_count = total_points
    
    for i, row in enumerate(merges_matrix):
        if current_cluster_count == num_clusters:
            break
            
        c1_id, c2_id = int(row[0]), int(row[1])
        new_id = total_points + i
        
        if c1_id not in cluster_to_points or c2_id not in cluster_to_points:
            continue
            
        new_points = cluster_to_points[c1_id].union(cluster_to_points[c2_id])
        cluster_to_points[new_id] = new_points
        
        for p_idx in new_points:
            point_to_cluster_id[p_idx] = new_id
            
        del cluster_to_points[c1_id]
        del cluster_to_points[c2_id]
        
        current_cluster_count -= 1

    # Attribution des labels simples
    labels = np.zeros(total_points, dtype=int)
    final_cluster_ids = list(cluster_to_points.keys()) 
    id_to_label = {id_: label for label, id_ in enumerate(final_cluster_ids)}
    
    for point_idx in range(total_points):
        current_id = point_to_cluster_id[point_idx]
        labels[point_idx] = id_to_label.get(current_id, 0)
        
    return labels

labels = get_cluster_labels_v2(Z, n_clusters, N_POINTS)

# Nuage initial
plt.figure(figsize=(6, 5)) 
plt.scatter(X[:, 0], X[:, 1], color='gray') 
plt.title("Nuage initial")
plt.show()

# Dendrogramme
plt.figure(figsize=(10, 6))
dendrogram(Z, 
           color_threshold=color_threshold_adjusted, 
           above_threshold_color='gray')
plt.axhline(y=color_threshold_adjusted, color='red', linestyle='--',
            label=f'Seuil pour {n_clusters} clusters')
plt.title("Dendrogramme (Méthode du Centroïde)")
plt.xlabel("Points initiaux")
plt.ylabel("Distance de fusion")
plt.legend()
plt.show()

# Nuage final coloré
plt.figure(figsize=(6, 5))
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='tab10', s=80) 
plt.title(f"Nuage de points : {n_clusters} clusters ")
plt.show()