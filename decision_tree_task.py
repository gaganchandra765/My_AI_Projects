# -*- coding: utf-8 -*-
"""Decision_Tree_task

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uIcE8vx8wMcpeQ9RmT0X67qrjjIc6IjF
"""

# decision_tree.py
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Step 1: Encode the Dataset
data = [
    [12.0, 1.5, 1, 'Wine'],
    [5.0, 2.0, 0, 'Beer'],
    [40.0, 0.0, 1, 'Whiskey'],
    [13.5, 1.2, 1, 'Wine'],
    [4.5, 1.8, 0, 'Beer'],
    [38.0, 0.1, 1, 'Whiskey'],
    [11.5, 1.7, 1, 'Wine'],
    [5.5, 2.3, 0, 'Beer']
]

# Convert labels to integers
label_map = {'Wine': 0, 'Beer': 1, 'Whiskey': 2}
inverse_label_map = {v: k for k, v in label_map.items()}

# Create X and y arrays
X = np.array([[row[0], row[1], row[2]] for row in data])
y = np.array([label_map[row[3]] for row in data])

class Node:
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, value=None):
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value  # For leaf nodes: class label

class DecisionTreeClassifier:
    def __init__(self, max_depth=3, min_samples_split=2, criterion='gini'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion = criterion
        self.root = None
        self.feature_names = ['Alcohol', 'Sugar', 'Color']

    def fit(self, X, y):
        self.root = self._grow_tree(X, y, depth=0)

    def _gini(self, y):
        counts = np.bincount(y)
        probabilities = counts / len(y)
        return 1 - np.sum(probabilities ** 2)

    def _entropy(self, y):
        counts = np.bincount(y)
        probabilities = counts / len(y)
        probabilities = probabilities[probabilities > 0]
        return -np.sum(probabilities * np.log2(probabilities))

    def _impurity(self, y):
        return self._gini(y) if self.criterion == 'gini' else self._entropy(y)

    def _best_split(self, X, y):
        n_samples, n_features = X.shape
        best_gain = -np.inf
        best_feature, best_threshold = None, None

        parent_impurity = self._impurity(y)

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_indices = X[:, feature] <= threshold
                right_indices = ~left_indices

                if sum(left_indices) < self.min_samples_split or sum(right_indices) < self.min_samples_split:
                    continue

                left_impurity = self._impurity(y[left_indices])
                right_impurity = self._impurity(y[right_indices])

                weighted_impurity = (sum(left_indices) * left_impurity + sum(right_indices) * right_impurity) / n_samples
                gain = parent_impurity - weighted_impurity

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _grow_tree(self, X, y, depth):
        n_samples = len(y)
        n_classes = len(np.unique(y))

        # Stopping criteria
        if (depth >= self.max_depth or n_classes == 1 or n_samples < self.min_samples_split):
            return Node(value=np.bincount(y).argmax())

        # Find best split
        feature, threshold = self._best_split(X, y)
        if feature is None:
            return Node(value=np.bincount(y).argmax())

        # Split data
        left_indices = X[:, feature] <= threshold
        right_indices = ~left_indices

        # Recursively build children
        left = self._grow_tree(X[left_indices], y[left_indices], depth + 1)
        right = self._grow_tree(X[right_indices], y[right_indices], depth + 1)

        return Node(feature, threshold, left, right)

    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])

    def _traverse_tree(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature_index] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)

    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        indent = "  " * depth
        if node.value is not None:
            print(f"{indent}Predict: {inverse_label_map[node.value]}")
        else:
            print(f"{indent}{self.feature_names[node.feature_index]} <= {node.threshold:.2f}")
            print(f"{indent}Left:")
            self.print_tree(node.left, depth + 1)
            print(f"{indent}Right:")
            self.print_tree(node.right, depth + 1)

    def visualize_decision_boundary(self, X, y):
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

        # Predict for color=0 and color=1 separately
        Z0 = self.predict(np.c_[xx.ravel(), yy.ravel(), np.zeros(xx.size)])
        Z1 = self.predict(np.c_[xx.ravel(), yy.ravel(), np.ones(xx.size)])

        Z0 = Z0.reshape(xx.shape)
        Z1 = Z1.reshape(xx.shape)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Color = 0
        ax1.contourf(xx, yy, Z0, alpha=0.4, cmap='viridis')
        scatter = ax1.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolor='k')
        ax1.set_title('Decision Boundary (Color=0)')
        ax1.set_xlabel('Alcohol Content (%)')
        ax1.set_ylabel('Sugar Content (g/L)')
        ax1.legend(handles=scatter.legend_elements()[0], labels=['Wine', 'Beer', 'Whiskey'])

        # Color = 1
        ax2.contourf(xx, yy, Z1, alpha=0.4, cmap='viridis')
        ax2.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis', edgecolor='k')
        ax2.set_title('Decision Boundary (Color=1)')
        ax2.set_xlabel('Alcohol Content (%)')
        ax2.set_ylabel('Sugar Content (g/L)')

        plt.tight_layout()
        plt.show()

# Step 6: Evaluation
test_data = np.array([
    [6.0, 2.1, 0],   # Expected: Beer
    [39.0, 0.05, 1], # Expected: Whiskey
    [13.0, 1.3, 1]   # Expected: Wine
])

# Train and evaluate with Gini
print("Training Decision Tree with Gini criterion...")
clf_gini = DecisionTreeClassifier(max_depth=3, min_samples_split=2, criterion='gini')
clf_gini.fit(X, y)
predictions_gini = clf_gini.predict(test_data)
print("\nTree Structure (Gini):")
clf_gini.print_tree()
print("\nPredictions (Gini):")
for i, pred in enumerate(predictions_gini):
    print(f"Test {i+1}: Predicted {inverse_label_map[pred]}, Expected {inverse_label_map[[1, 2, 0][i]]}")
clf_gini.visualize_decision_boundary(X, y)

# Train and evaluate with Entropy
print("\nTraining Decision Tree with Entropy criterion...")
clf_entropy = DecisionTreeClassifier(max_depth=3, min_samples_split=2, criterion='entropy')
clf_entropy.fit(X, y)
predictions_entropy = clf_entropy.predict(test_data)
print("\nTree Structure (Entropy):")
clf_entropy.print_tree()
print("\nPredictions (Entropy):")
for i, pred in enumerate(predictions_entropy):
    print(f"Test {i+1}: Predicted {inverse_label_map[pred]}, Expected {inverse_label_map[[1, 2, 0][i]]}")
clf_entropy.visualize_decision_boundary(X, y)

