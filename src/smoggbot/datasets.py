"""Synthetic dataset generators and a train/test splitter (NumPy only)."""

from __future__ import annotations

import numpy as np


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.25,
    random_state: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split arrays into train and test subsets (shuffled, seeded)."""
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size must be between 0 and 1")
    X = np.asarray(X)
    y = np.asarray(y)
    rng = np.random.default_rng(random_state)
    idx = rng.permutation(X.shape[0])
    n_test = int(X.shape[0] * test_size)
    test_idx, train_idx = idx[:n_test], idx[n_test:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def make_regression(
    n_samples: int = 200,
    n_features: int = 3,
    noise: float = 1.0,
    random_state: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Linear data: y = X @ true_coef + noise. Returns (X, y, true_coef)."""
    rng = np.random.default_rng(random_state)
    X = rng.normal(size=(n_samples, n_features))
    true_coef = rng.uniform(-5, 5, size=n_features)
    y = X @ true_coef + rng.normal(scale=noise, size=n_samples)
    return X, y, true_coef


def make_classification(
    n_samples: int = 300,
    n_features: int = 2,
    n_classes: int = 2,
    separation: float = 3.0,
    random_state: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """Gaussian blobs, one per class. Returns (X, y)."""
    rng = np.random.default_rng(random_state)
    per_class = n_samples // n_classes
    angles = np.linspace(0, 2 * np.pi, n_classes, endpoint=False)
    centers = np.stack(
        [separation * np.cos(angles), separation * np.sin(angles)], axis=1
    )
    # Pad centres with zeros if more than 2 features are requested.
    if n_features > 2:
        centers = np.pad(centers, ((0, 0), (0, n_features - 2)))
    Xs, ys = [], []
    for c in range(n_classes):
        n_c = per_class + (n_samples % n_classes if c == 0 else 0)
        Xs.append(rng.normal(loc=centers[c], scale=1.0, size=(n_c, n_features)))
        ys.append(np.full(n_c, c))
    return np.vstack(Xs), np.concatenate(ys)


def make_blobs(
    n_samples: int = 300,
    n_features: int = 2,
    n_blobs: int = 3,
    spread: float = 1.0,
    random_state: int = 0,
) -> np.ndarray:
    """Unlabelled Gaussian blobs for clustering experiments."""
    X, _ = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_classes=n_blobs,
        separation=4.0,
        random_state=random_state,
    )
    rng = np.random.default_rng(random_state + 1)
    return X + rng.normal(scale=spread - 1.0 if spread > 1 else 0.0, size=X.shape)
