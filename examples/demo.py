"""End-to-end demo: train and evaluate every model in smoggbot.

Run from the project root::

    python examples/demo.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np

from smoggbot import LinearRegression, KNNClassifier, KMeans, datasets, metrics


def demo_regression() -> None:
    print("=" * 60)
    print("LINEAR REGRESSION (normal equation)")
    print("=" * 60)
    X, y, true_coef = datasets.make_regression(
        n_samples=500, n_features=3, noise=0.5, random_state=42
    )
    X_train, X_test, y_train, y_test = datasets.train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LinearRegression().fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"true coefficients : {np.round(true_coef, 3)}")
    print(f"learned coefficients: {np.round(model.coef_, 3)}")
    print(f"MSE : {metrics.mean_squared_error(y_test, preds):.4f}")
    print(f"R^2 : {metrics.r2_score(y_test, preds):.4f}\n")


def demo_knn() -> None:
    print("=" * 60)
    print("k-NEAREST NEIGHBOURS CLASSIFIER")
    print("=" * 60)
    X, y = datasets.make_classification(
        n_samples=400, n_features=2, n_classes=3, random_state=7
    )
    X_train, X_test, y_train, y_test = datasets.train_test_split(
        X, y, test_size=0.25, random_state=7
    )
    for k in (1, 5, 15):
        model = KNNClassifier(k=k).fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = metrics.accuracy_score(y_test, preds)
        print(f"k={k:<2d}  accuracy: {acc:.4f}")
    print()


def demo_kmeans() -> None:
    print("=" * 60)
    print("k-MEANS CLUSTERING")
    print("=" * 60)
    X = datasets.make_blobs(
        n_samples=300, n_features=2, n_blobs=3, spread=1.0, random_state=11
    )
    model = KMeans(n_clusters=3, random_state=11).fit(X)
    print(f"converged in {model.n_iter_} iterations")
    print(f"inertia   : {model.inertia_:.2f}")
    print(f"centroids :\n{np.round(model.cluster_centers_, 3)}\n")


if __name__ == "__main__":
    demo_regression()
    demo_knn()
    demo_kmeans()
