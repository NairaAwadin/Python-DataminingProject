"""
** Datamining Project : KNN Algorithm
** Dataset : Iris Dataset - PATH = dataset/iris.csv
** Description : Ce programme utilise l algorithme KNN pour prédire la classe d un échantillon du dataset Iris en se basant sur ses voisins les plus proches.
** Contributors : Leo, Yane, Paul, Mika et Naira
** Date : 19/10/2025
"""
from math import sqrt
import matplotlib.pyplot as plt
import csv

def euclidean_distance(point_a, point_b):
    distance = 0
    for i in range(len(point_a) - 1): # on ingnore la derniere colone (le label)
        distance = distance + (point_a[i] - point_b[i]) ** 2
    return sqrt(distance)

def predict_knn_classe(dataset, test_point, k):
    distances = []
    for row in dataset: # calcul de distance entre le pt_test et chaque ligne du dataset
        dist = euclidean_distance(test_point, row)
        distances.append((dist, row[-1])) # liste de tuples
    distances.sort() # on trie les dists par ordre croissant
    k_classes = [] # stock les classes des k plus proches voisisns

    for i in range(k):
        k_classes.append(distances[i][1])
    max_count = 0
    prediction = None

    for classe in set(k_classes): # on regarde chaque classe unique
        count = k_classes.count(classe)  # puis on compte cmb de fois il apparait
        if count > max_count:
            max_count = count
            prediction = classe # classe la plus fréquente
    return prediction

def load_dataset(filepath):
    dataset = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # ignorer l’en-tete
        for row in reader:
            dataset.append([float(row[0]), float(row[1]), float(row[2]), float(row[3]), row[4]])
    return dataset

# evaluation pour mesurer la performance de l'algo

def evaluate_knn(dataset, k):
    nb_correct_pred = 0
    for row in dataset:
        if predict_knn_classe(dataset, row, k) == row[-1]: # on predit la classe du pt et on compare avec la vraie
            nb_correct_pred = nb_correct_pred + 1

    evaluation = nb_correct_pred / len(dataset)
    return evaluation

# Visualisaiton 2D

def visualisation_knn(dataset, test_points, predictions, evaluation):
    plt.figure(figsize=(8,6))

    classes = sorted(set(row[-1] for row in dataset)) #recupere les classes dans l'ordre alphabetique
    palette = ['mediumpurple', 'skyblue', 'lightgreen', 'salmon']
    colors = {} # dictionnaire vide

    for i, cls in enumerate(classes):  # enumerate() renvoi index et classe correspondant -> on parcourt les classs et leur index
        color = palette[i % len(palette)]  # on choisit une couleur selon l’index et on recommence si on a + de cls que de couleurs
        colors[cls] = color  # remplissage du dictionnaire petit à petit avec les paires

    for row in dataset:
        x, y, _, _, label = row
        plt.scatter(x, y, color=colors[label], s=60, alpha=0.8, edgecolors='black')

    # points test
    for p, pred in zip(test_points, predictions): # pour chaque pt test et sa prediction
        plt.scatter(p[0], p[1], color=colors[pred], marker='X', s=180, edgecolors='black', linewidths=1.5)
        plt.text(p[0] + 0.1, p[1] + 0.05, f"prediction={pred}", fontsize=9, weight='bold')

    # légende
    for cls in classes:
        plt.scatter([], [], color=colors[cls], edgecolors='black', label=cls)

    plt.title(f"KNN : visualisation simple sur le dataset Iris (evaluation={evaluation*100:.2f}%)")
    plt.xlabel("Longueur des sépales")
    plt.ylabel("Largeur des sépales")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()


dataset = load_dataset("dataset/iris.csv")

test_points = [
    [5.1, 3.5, 1.4, 0.2, None],  # ressemble à Setosa
    [6.2, 2.8, 4.8, 1.8, None],  # ressemble à Virginica
    [5.5, 2.5, 4.0, 1.3, None]   # ressemble à Versicolor
]

predictions = [predict_knn_classe(dataset, p, 5) for p in test_points]
evaluation = evaluate_knn(dataset, 5)

print("Prédictions :", predictions)
print(f"Taux de réussite : {evaluation*100:.2f}%")

visualisation_knn(dataset, test_points, predictions, evaluation)
