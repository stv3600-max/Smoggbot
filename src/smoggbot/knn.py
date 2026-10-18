"""k-Nearest Neighbours classifier, implemented from scratch.

Classification is by majority vote of the k closest training points
under Euclidean distance. Ties are broken by the smallest class label.
"""

from __future__ import annotations

import numpy as np


class KNNClassifier:
    """k-NN classifier.

    Parameters
    ----------
    k:
        Number of neighbours to consult. Must be a positive integer.

    Attributes
    ----------
    classes_:
        Sorted unique class labels seen during ``fit``.
    """

    def __init__(self, k: int = 5) -> None:
        if not isinstance(k, int) or k < 1:
            raise ValueError("k must be a positive integer")
        self.k = k
        self._X: np.ndarray | None = None
        self._y: np.ndarray | None = None
        self.classes_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        """Memorise the training set (k-NN is a lazy learner)."""
        self._X = np.asarray(X, dtype=float)
        self._y = np.asarray(y).ravel()
        if self._X.shape[0] != self._y.shape[0]:
            raise ValueError("X and y have inconsistent lengths")
        if self.k > self._X.shape[0]:
            raise ValueError("k cannot exceed the number of training samples")
        self.classes_ = np.unique(self._y)
        return self

    def _check_fitted(self) -> None:
        if self._X is None or self._y is None:
            raise RuntimeError("Model is not fitted yet; call fit() first.")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for X by majority vote of neighbours."""
        self._check_fitted()
        assert self._X is not None and self._y is not None
        X = np.asarray(X, dtype=float)
        # Pairwise squared Euclidean distances, computed without an
        # explicit Python loop: ||a - b||^2 = ||a||^2 + ||b||^2 - 2 a.b
        x_norm = np.sum(X**2, axis=1, keepdims=True)
        t_norm = np.sum(self._X**2, axis=1)
        dists = x_norm + t_norm - 2.0 * (X @ self._X.T)
        np.maximum(dists, 0.0, out=dists)  # guard against fp noise
        neighbour_idx = np.argpartition(dists, self.k - 1, axis=1)[:, : self.k]
        neighbour_labels = self._y[neighbour_idx]
        # Majority vote; np.bincount breaks ties toward the smallest label
        # once labels are mapped to 0..C-1 via the sorted classes_.
        label_to_idx = {c: i for i, c in enumerate(self.classes_)}
        mapped = np.vectorize(label_to_idx.__getitem__)(neighbour_labels)
        votes = np.apply_along_axis(
            lambda row: np.bincount(row, minlength=len(self.classes_)), 1, mapped
        )
        return self.classes_[np.argmax(votes, axis=1)]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Fraction of the k neighbours belonging to each class."""
        self._check_fitted()
        assert self._X is not None and self._y is not None
        X = np.asarray(X, dtype=float)
        x_norm = np.sum(X**2, axis=1, keepdims=True)
        t_norm = np.sum(self._X**2, axis=1)
        dists = x_norm + t_norm - 2.0 * (X @ self._X.T)
        np.maximum(dists, 0.0, out=dists)
        neighbour_idx = np.argpartition(dists, self.k - 1, axis=1)[:, : self.k]
        neighbour_labels = self._y[neighbour_idx]
        label_to_idx = {c: i for i, c in enumerate(self.classes_)}
        mapped = np.vectorize(label_to_idx.__getitem__)(neighbour_labels)
        counts = np.apply_along_axis(
            lambda row: np.bincount(row, minlength=len(self.classes_)), 1, mapped
        )
        return counts / self.k
