"""Evaluation metrics for classification and regression, from scratch."""

from __future__ import annotations

import numpy as np


def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Fraction of correctly predicted labels."""
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    return float(np.mean(y_true == y_pred))


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Confusion matrix with rows = true labels, columns = predicted labels."""
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    classes = np.unique(np.concatenate([y_true, y_pred]))
    idx = {c: i for i, c in enumerate(classes)}
    cm = np.zeros((len(classes), len(classes)), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[idx[t], idx[p]] += 1
    return cm


def _binary_counts(
    y_true: np.ndarray, y_pred: np.ndarray, pos_label
) -> tuple[int, int, int]:
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    tp = int(np.sum((y_true == pos_label) & (y_pred == pos_label)))
    fp = int(np.sum((y_true != pos_label) & (y_pred == pos_label)))
    fn = int(np.sum((y_true == pos_label) & (y_pred != pos_label)))
    return tp, fp, fn


def precision_score(
    y_true: np.ndarray, y_pred: np.ndarray, pos_label=1
) -> float:
    """TP / (TP + FP); 0.0 when the denominator is 0."""
    tp, fp, _ = _binary_counts(y_true, y_pred, pos_label)
    return tp / (tp + fp) if (tp + fp) > 0 else 0.0


def recall_score(y_true: np.ndarray, y_pred: np.ndarray, pos_label=1) -> float:
    """TP / (TP + FN); 0.0 when the denominator is 0."""
    tp, _, fn = _binary_counts(y_true, y_pred, pos_label)
    return tp / (tp + fn) if (tp + fn) > 0 else 0.0


def f1_score(y_true: np.ndarray, y_pred: np.ndarray, pos_label=1) -> float:
    """Harmonic mean of precision and recall; 0.0 when both are 0."""
    p = precision_score(y_true, y_pred, pos_label)
    r = recall_score(y_true, y_pred, pos_label)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean of squared residuals."""
    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    return float(np.mean((y_true - y_pred) ** 2))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Coefficient of determination: 1 - SS_res / SS_tot."""
    y_true = np.asarray(y_true, dtype=float).ravel()
    y_pred = np.asarray(y_pred, dtype=float).ravel()
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
