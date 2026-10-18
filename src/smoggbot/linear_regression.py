"""Ordinary least squares linear regression, implemented from scratch.

The closed-form (normal equation) solution is used:

    w = (X^T X)^-1 X^T y

solved via ``numpy.linalg.lstsq`` for numerical stability.
An intercept term is fitted by default.
"""

from __future__ import annotations

import numpy as np


class LinearRegression:
    """Linear regression fitted with the normal equation.

    Parameters
    ----------
    fit_intercept:
        If True, a bias (intercept) column of ones is added to the
        design matrix before fitting.

    Attributes
    ----------
    coef_:
        Estimated coefficients of shape (n_features,).
    intercept_:
        Fitted intercept (0.0 when ``fit_intercept=False``).
    """

    def __init__(self, fit_intercept: bool = True) -> None:
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def _design(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if self.fit_intercept:
            return np.column_stack([np.ones(X.shape[0]), X])
        return X

    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        """Fit the model to training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
        y : array-like of shape (n_samples,)
        """
        Xd = self._design(X)
        y = np.asarray(y, dtype=float).ravel()
        if Xd.shape[0] != y.shape[0]:
            raise ValueError("X and y have inconsistent lengths")
        w, *_ = np.linalg.lstsq(Xd, y, rcond=None)
        if self.fit_intercept:
            self.intercept_ = float(w[0])
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values for X."""
        if self.coef_ is None:
            raise RuntimeError("Model is not fitted yet; call fit() first.")
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        return X @ self.coef_ + self.intercept_
