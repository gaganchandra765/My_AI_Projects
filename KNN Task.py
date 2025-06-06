# -*- coding: utf-8 -*-
"""EpochSpringCampSupervisedLearnigTasks.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VPu3X7g3LEo0XF8p-Iqy-Z45DXBzxb32

# Initial Data preparation
"""

import numpy as np


data = [
    [150, 7.0, 1, 'Apple'],
    [120, 6.5, 0, 'Banana'],
    [180, 7.5, 2, 'Orange'],
    [155, 7.2, 1, 'Apple'],
    [110, 6.0, 0, 'Banana'],
    [190, 7.8, 2, 'Orange'],
    [145, 7.1, 1, 'Apple'],
    [115, 6.3, 0, 'Banana']
]

"""Preparing X(Feature Matrix) and Y (Label Vector) from our data matrix , We have used Label encoding"""

Y = [array[3] for array in data]
X = [array[:-1] for array in data]


# Mapping from word to number
mapping = {'Apple': 1, 'Banana': 0, 'Orange': 2}

# Replace using list comprehension
Y = [mapping.get(word, word) for word in Y]

print("Y :", Y)
print("X = ",X)
X = np.array(X)
X_2d = X[:, [0, 1]]  # Shape: (8, 2), only weight and size

# Test data (2D)
test_data_2d = np.array([
    [118, 6.2],  # Banana
    [160, 7.3],  # Apple
    [185, 7.7]   # Orange
])
"""Defining Euclidean Distance (The Metric to measure closeness)"""

def euclideanDistance(array1,array2):
    distance = 0
    for i in range(len(array1)):
        distance += (array1[i] - array2[i])**2
    return distance**0.5

"""# Building the KNN class"""

import numpy as np

class KNN:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict_one(self, x):
        # Compute Euclidean distances using NumPy broadcasting
        distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))

        # Get indices of k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k nearest neighbors
        k_labels = self.y_train[k_indices]

        # Find the most common label using NumPy
        unique_labels, counts = np.unique(k_labels, return_counts=True)
        most_common = unique_labels[np.argmax(counts)]

        return most_common

    def predict(self, X_test):
        X_test = np.array(X_test)
        return np.array([self.predict_one(x) for x in X_test])

"""Running our KNN operation on the the input data itself"""

knn = KNN(k=3)
knn.fit(X, Y)
predictions = knn.predict(X)
print(predictions)

"""# Testing the KNN on our Testing data set"""

test_data = np.array([
    [118, 6.2, 0],  # Expected: Banana
    [160, 7.3, 1],  # Expected: Apple
    [185, 7.7, 2]   # Expected: Orange
])
TestDataPredictions = knn.predict(test_data)
print(TestDataPredictions)
k_values = [1,3,5]
ExpectedOutputs= [0,1,2]
for k in k_values:
      knn = KNN(k=k)
      knn.fit(X, Y)
      predictions = knn.predict(test_data)
      print(f"Predictions for k={k}: {predictions}")
      accuracy = np.mean(predictions == ExpectedOutputs)
      print(f"Accuracy for k={k}: {accuracy}")

"""# Bonus: Normalization of the features

## Min - Max Normalization
"""

def min_max_normalize(X):
    X = np.array(X)
    min_vals = X.min(axis=0)
    max_vals = X.max(axis=0)
    return (X - min_vals) / (max_vals - min_vals)
new_knn = KNN(k=3)
new_knn.fit(min_max_normalize(X), Y)
predictions = new_knn.predict(min_max_normalize(test_data))
print(predictions)

"""## Z-Score Normalization"""

def z_score_normalize(X):
    X = np.array(X)
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    return (X - mean) / std
new_knn = KNN(k=3)
new_knn.fit(z_score_normalize(X), Y)
predictions = new_knn.predict(z_score_normalize(test_data))
print(predictions)

"""# Trying different distance metrics

## Manhattan
"""

class KNN_Manhattan:
    def __init__(self, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict_one(self, x):
        # Compute Euclidean distances using NumPy broadcasting
        distances = np.sum(np.abs(self.X_train - x), axis=1)

        # Get indices of k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k nearest neighbors
        k_labels = self.y_train[k_indices]

        # Find the most common label using NumPy
        unique_labels, counts = np.unique(k_labels, return_counts=True)
        most_common = unique_labels[np.argmax(counts)]

        return most_common

    def predict(self, X_test):
        X_test = np.array(X_test)
        return np.array([self.predict_one(x) for x in X_test])

knn_man = KNN_Manhattan(k=3)
knn_man.fit(X, Y)
predictions = knn_man.predict(test_data)
print(predictions)

"""## Minkowski"""

class KNN_Minkowski:
    def __init__(self,p, k=3):
        self.k = k
        self.X_train = None
        self.y_train = None
        self.p = p

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict_one(self, x):
        # Compute Euclidean distances using NumPy broadcasting
        distances = np.sum(np.abs(self.X_train - x) ** self.p, axis=1) ** (1 / self.p)

        # Get indices of k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]

        # Get the labels of the k nearest neighbors
        k_labels = self.y_train[k_indices]

        # Find the most common label using NumPy
        unique_labels, counts = np.unique(k_labels, return_counts=True)
        most_common = unique_labels[np.argmax(counts)]

        return most_common

    def predict(self, X_test):
        X_test = np.array(X_test)
        return np.array([self.predict_one(x) for x in X_test])

knn_mink = KNN_Minkowski(k=3,p=4)
knn_mink.fit(X, Y)
predictions = knn_mink.predict(test_data)
print(predictions)

"""# Visualization of Decision Boundaries"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# KNN class with distance metrics
class KNN:
    def __init__(self, k=3, distance='euclidean', p=3):
        self.k = k
        self.distance = distance
        self.p = p

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def compute_distance(self, x):
        if self.distance == 'euclidean':
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        elif self.distance == 'manhattan':
            return np.sum(np.abs(self.X_train - x), axis=1)
        elif self.distance == 'minkowski':
            return np.sum(np.abs(self.X_train - x) ** self.p, axis=1) ** (1 / self.p)
        else:
            raise ValueError("Unsupported distance metric")

    def predict_one(self, x):
        distances = self.compute_distance(x)
        k_indices = np.argsort(distances)[:self.k]
        k_labels = self.y_train[k_indices]
        unique_labels, counts = np.unique(k_labels, return_counts=True)
        return unique_labels[np.argmax(counts)]

    def predict(self, X_test):
        return np.array([self.predict_one(x) for x in X_test])

# Normalization
def min_max_normalize(X):
    X = np.array(X)
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

# Data: [weight, size, color], we only use [weight, size] for visualization

# Normalize features
X_norm = min_max_normalize(X_2d)

# Grid for visualization
h = 0.01
x_min, x_max = X_norm[:, 0].min() - 0.1, X_norm[:, 0].max() + 0.1
y_min, y_max = X_norm[:, 1].min() - 0.1, X_norm[:, 1].max() + 0.1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
grid_points = np.c_[xx.ravel(), yy.ravel()]

# Plot decision boundary
def plot_decision_boundary(k=3, distance='euclidean', p=3):
    knn = KNN(k=k, distance=distance, p=p)
    knn.fit(X_norm, Y)
    Z = knn.predict(grid_points)
    Z = Z.reshape(xx.shape)

    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ['red', 'green', 'blue']

    plt.figure(figsize=(6, 5))
    plt.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.7)
    for i, color in zip(range(3), cmap_bold):
        plt.scatter(X_norm[Y == i][:, 0], X_norm[Y == i][:, 1],
                    label=f'Class {i}', color=color, edgecolor='k', s=60)
    plt.title(f"Decision Boundary (k={k}, metric={distance})")
    plt.xlabel("Normalized Weight")
    plt.ylabel("Normalized Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Try with different metrics
plot_decision_boundary(k=3, distance='euclidean')
plot_decision_boundary(k=3, distance='manhattan')
plot_decision_boundary(k=3, distance='minkowski', p=3)

"""# Weighted KNN"""

import numpy as np

class WeightedKNN:
    def __init__(self, k=3, distance='euclidean', p=3):
        self.k = k
        self.distance = distance
        self.p = p

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def compute_distance(self, x):
        if self.distance == 'euclidean':
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        elif self.distance == 'manhattan':
            return np.sum(np.abs(self.X_train - x), axis=1)
        elif self.distance == 'minkowski':
            return np.sum(np.abs(self.X_train - x) ** self.p, axis=1) ** (1 / self.p)
        else:
            raise ValueError("Unsupported distance metric")

    def predict_one(self, x):
        distances = self.compute_distance(x)
        # Avoid division by zero by adding a small epsilon
        epsilon = 1e-10
        k_indices = np.argsort(distances)[:self.k]
        k_distances = distances[k_indices]
        k_labels = self.y_train[k_indices]

        # Compute weights as inverse of distances
        weights = 1 / (k_distances + epsilon)

        # Aggregate weighted votes for each class
        unique_labels = np.unique(self.y_train)
        weighted_votes = np.zeros(len(unique_labels))

        for i, label in enumerate(unique_labels):
            label_mask = k_labels == label
            weighted_votes[i] = np.sum(weights[label_mask])

        # Return the label with the highest weighted vote
        return unique_labels[np.argmax(weighted_votes)]

    def predict(self, X_test):
        return np.array([self.predict_one(x) for x in X_test])

knn_we = WeightedKNN(k=3)
knn_we.fit(X_2d, Y)
predictions = knn_we.predict(test_data_2d)
print(predictions)

"""## Visualizing The Decision Boundaries , using WeightedKNN"""

def plot_decision_boundary(k=3, distance='euclidean', p=3):
    knn_we = WeightedKNN(k=k, distance=distance, p=p)
    knn_we.fit(X_norm, Y)
    Z = knn_we.predict(grid_points)
    Z = Z.reshape(xx.shape)

    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
    cmap_bold = ['red', 'green', 'blue']

    plt.figure(figsize=(6, 5))
    plt.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.7)
    for i, color in zip(range(3), cmap_bold):
        plt.scatter(X_norm[Y == i][:, 0], X_norm[Y == i][:, 1],
                    label=f'Class {i}', color=color, edgecolor='k', s=60)
    plt.title(f"Decision Boundary (k={k}, metric={distance})")
    plt.xlabel("Normalized Weight")
    plt.ylabel("Normalized Size")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Try with different metrics
plot_decision_boundary(k=3, distance='euclidean')
plot_decision_boundary(k=3, distance='manhattan')
plot_decision_boundary(k=3, distance='minkowski', p=3)