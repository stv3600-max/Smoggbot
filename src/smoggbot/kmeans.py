"""k-Means clustering, implemented from scratch (Lloyd's algorithm).

Centroids are initialised by sampling training points uniformly at
random (seeded for reproducibility), then alternately re-assigned and
recomputed until assignments stop changing or ``max_iter`` is reached.
"""

from __future__ import annotations

import numpy as np


class KMeans:
    """k-Means clustering.

    Parameters
    ----------
    n_clusters:
        Number of clusters. Must be a positive integer.
    max_iter:
        Maximum Lloyd iterations.
    tol:
        Convergence tolerance on the shift of the centroids
        (Frobenius norm) between iterations.
    random_state:
        Seed for centroid initialisation.

    Attributes
    ----------
    cluster_centers_:
        Final centroids of shape (n_clusters, n_features).
    labels_:
        Cluster index assigned to each training sample.
    inertia_:
        Sum of squared distances of samples to their closest centroid.
    n_iter_:
        Number of iterations actually run.
    """

    def __init__(
        self,
        n_clusters: int = 3,
        max_iter: int = 300,
        tol: float = 1e-4,
        random_state: int = 0,
    ) -> None:
        if not isinstance(n_clusters, int) or n_clusters < 1:
            raise ValueError("n_clusters must be a positive integer")
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.cluster_centers_: np.ndarray | None = None
        self.labels_: np.ndarray | None = None
        self.inertia_: float | None = None
        self.n_iter_: int = 0

    def _assign(self, X: np.ndarray, centers: np.ndarray) -> np.ndarray:
        dists = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2)
        return np.argmin(dists, axis=1)

    def fit(self, X: np.ndarray) -> "KMeans":
        """Compute centroids from training data X."""
        X = np.asarray(X, dtype=float)
        n_samples = X.shape[0]
        if self.n_clusters > n_samples:
            raise ValueError("n_clusters cannot exceed number of samples")
        rng = np.random.default_rng(self.random_state)
        init_idx = rng.choice(n_samples, size=self.n_clusters, replace=False)
        centers = X[init_idx].copy()

        labels = np.full(n_samples, -1)
        for i in range(1, self.max_iter + 1):
            new_labels = self._assign(X, centers)
            new_centers = np.array(
                [
                    X[new_labels == j].mean(axis=0)
                    if np.any(new_labels == j)
                    else centers[j]  # keep centroid if cluster is empty
                    for j in range(self.n_clusters)
                ]
            )
            shift = np.linalg.norm(new_centers - centers)
            centers, labels = new_centers, new_labels
            self.n_iter_ = i
            if shift <= self.tol:
                break

        self.cluster_centers_ = centers
        self.labels_ = labels
        self.inertia_ = float(
            np.sum((X - centers[labels]) ** 2)
        )
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Assign each sample in X to the nearest centroid."""
        if self.cluster_centers_ is None:
            raise RuntimeError("Model is not fitted yet; call fit() first.")
        return self._assign(np.asarray(X, dtype=float), self.cluster_centers_)
