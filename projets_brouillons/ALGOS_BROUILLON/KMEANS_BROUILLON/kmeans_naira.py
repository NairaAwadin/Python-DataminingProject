import random
from math import sqrt

def euclidean_distance(point_a, point_b):
	distance = 0
	for i in range(len(point_a) - 1):
		distance = distance + (point_a[i] - point_b[i])** 2
	return sqrt(distance)

def init_centroids(dataset, k):
    centroids = random.sample(dataset, k) # choisit les k pts aleatoire dans la dataset comme centroids initiaux
    return centroids

def assign_clusters(dataset, centroids):
    clusters = []
    for _ in centroids:
        clusters.append([]) #un cluster vide pour chaque centroid
    for point in dataset:
        distances = []
        for centroid in centroids: # on calcul la distance du point a tt les centroids
            d = euclidean_distance(point, centroid)
            distances.append(d) #notre liste de distances

        min_distance = min(distances) # on prend la plus petite distance / centroid le plus proche

        closest_index = distances.index(min_distance)  # index va nous donner la position de cette distance

        clusters[closest_index].append(point) # on prend le pt et on l'ajoute au cluster qui correspond au centroid
    return clusters

def update_centroids(clusters): #on recalcule le centroid de chaque cluster en faisant la moyenne des coordonnées
    new_centroids = []
    for cluster in clusters:
        sum_x = sum(point[0] for point in cluster) #somme des coordonnées x
        sum_y = sum(point[1] for point in cluster) #somme des coordonnées y
        n_points = len(cluster)
        new_centroid = [sum_x / n_points, sum_y / n_points] #calcul moyenne des coordonnées
        new_centroids.append(new_centroid) #on sauvegarde le nv centroid du cluster
    return new_centroids

def kmeans(dataset, k, max_iters=10):
    centroids = init_centroids(dataset, k)
    for _ in range(max_iters): # pour eviter une boucle inf
        clusters = assign_clusters(dataset, centroids)
        new_centroids = update_centroids(clusters)
        # Vérification simple : si les centroids ne changent pas, on arrête
        if new_centroids == centroids:
            print("Convergence atteinte !")
            break
        centroids = new_centroids
    return centroids, clusters

dataset = [
    [2.78, 2.55],
    [1.47, 2.36],
    [3.40, 4.40],
    [1.39, 1.85],
    [3.06, 3.01],
    [7.63, 2.76],
    [5.33, 2.09],
    [6.92, 1.77],
    [8.68, -0.24],
    [7.67, 3.51]
]

k = 3
'''centroids = init_centroids(dataset, k)
clusters = assign_clusters(dataset, centroids)

print("Clusters après assignation :")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: {cluster}")'''

centroids, clusters = kmeans(dataset, k)

print("Centroids finaux :")
for i, centroid in enumerate(centroids):
    print(f"Centroid {i+1}: {centroid}")

print("\nClusters finaux :")
for i, cluster in enumerate(clusters):
    print(f"Cluster {i+1}: {cluster}")