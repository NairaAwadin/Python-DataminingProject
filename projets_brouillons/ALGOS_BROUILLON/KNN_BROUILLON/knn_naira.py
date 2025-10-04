'''
distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
'''
from math import sqrt

def euclidean_distance(point_a, point_b):
	distance = 0
	for i in range(len(point_a) - 1):
		distance = distance + (point_a[i] - point_b[i])** 2
	return sqrt(distance)

def knn_predict(training_data, test_point, k):
    distances = []
    for row in training_data: #calcul de toutes les distances
        dist = euclidean_distance(test_point, row)
        distances.append((dist, row[-1]))  # (distance, label)

    distances.sort()  #trie des distance par ordre croissant, les pts les plus proches du poinnt test sont au debut

    k_labels = []
    for i in range(k):
        k_labels.append(distances[i][1])  #distances[i][1] = label et Pour chacun, on ajoute le label du voisin à k_labels

    #ici on veut trouver la class majoritaire
    max_count = 0
    prediction = None
    for label in set(k_labels): # on regarde chaque label unique
        count = k_labels.count(label)  # puis on compte cmb de fois il apparait
        if count > max_count:
            max_count = count
            prediction = label

    return prediction
dataset = [
    [2.78, 2.55, 0],
    [1.47, 2.36, 0],
    [3.40, 4.40, 1],
    [1.39, 1.85, 1],
    [3.06, 3.01, 1],
    [7.63, 2.76, 1],
    [5.33, 2.09, 1],
    [6.92, 1.77, 1],
    [8.68, -0.24, 1],
    [7.67, 3.51, 1]
]
point_0 = dataset[0]
for point in dataset:
	distance = euclidean_distance(point_0, point)
	print(distance)

test_point = [3.0, 3.5, None]  # point à classer
print("Prediction:", knn_predict(dataset, test_point, 3))