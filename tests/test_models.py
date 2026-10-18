"""Unit tests for smoggbot (standard library only: ``python -m unittest``)."""

import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from smoggbot import LinearRegression, KNNClassifier, KMeans, datasets, metrics


class TestLinearRegression(unittest.TestCase):
    def test_recovers_true_coefficients(self):
        X, y, true_coef = datasets.make_regression(
            n_samples=300, n_features=2, noise=0.01, random_state=0
        )
        model = LinearRegression().fit(X, y)
        np.testing.assert_allclose(model.coef_, true_coef, atol=0.1)

    def test_perfect_fit_on_noiseless_line(self):
        X = np.arange(10, dtype=float).reshape(-1, 1)
        y = 3.0 * X.ravel() + 2.0
        model = LinearRegression().fit(X, y)
        np.testing.assert_allclose(model.predict(X), y, atol=1e-8)

    def test_not_fitted_raises(self):
        with self.assertRaises(RuntimeError):
            LinearRegression().predict(np.zeros((2, 2)))


class TestKNNClassifier(unittest.TestCase):
    def setUp(self):
        X, y = datasets.make_classification(
            n_samples=200, n_features=2, n_classes=2, separation=4.0, random_state=1
        )
        self.X_train, self.X_test, self.y_train, self.y_test = (
            datasets.train_test_split(X, y, test_size=0.3, random_state=1)
        )

    def test_high_accuracy_on_separated_blobs(self):
        preds = KNNClassifier(k=5).fit(self.X_train, self.y_train).predict(self.X_test)
        self.assertGreaterEqual(metrics.accuracy_score(self.y_test, preds), 0.95)

    def test_proba_rows_sum_to_one(self):
        model = KNNClassifier(k=5).fit(self.X_train, self.y_train)
        proba = model.predict_proba(self.X_test)
        np.testing.assert_allclose(proba.sum(axis=1), 1.0, atol=1e-8)

    def test_invalid_k_raises(self):
        with self.assertRaises(ValueError):
            KNNClassifier(k=0)


class TestKMeans(unittest.TestCase):
    def test_finds_three_blobs(self):
        X = datasets.make_blobs(n_samples=150, n_blobs=3, random_state=3)
        model = KMeans(n_clusters=3, random_state=3).fit(X)
        self.assertEqual(len(np.unique(model.labels_)), 3)
        # Each centroid should sit close to a true blob centre.
        self.assertLess(model.inertia_, 600.0)

    def test_predict_matches_labels(self):
        X = datasets.make_blobs(n_samples=60, n_blobs=2, random_state=4)
        model = KMeans(n_clusters=2, random_state=4).fit(X)
        np.testing.assert_array_equal(model.predict(X), model.labels_)

    def test_too_many_clusters_raises(self):
        with self.assertRaises(ValueError):
            KMeans(n_clusters=10).fit(np.zeros((5, 2)))


class TestMetrics(unittest.TestCase):
    def test_binary_scores(self):
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_pred = np.array([1, 0, 0, 0, 1, 1])
        self.assertAlmostEqual(metrics.accuracy_score(y_true, y_pred), 4 / 6)
        self.assertAlmostEqual(metrics.precision_score(y_true, y_pred), 2 / 3)
        self.assertAlmostEqual(metrics.recall_score(y_true, y_pred), 2 / 3)
        self.assertAlmostEqual(metrics.f1_score(y_true, y_pred), 2 / 3)

    def test_regression_scores(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(metrics.mean_squared_error(y_true, y_pred), 0.0)
        self.assertAlmostEqual(metrics.r2_score(y_true, y_pred), 1.0)

    def test_confusion_matrix_shape(self):
        cm = metrics.confusion_matrix([0, 1, 1, 2], [0, 1, 2, 2])
        self.assertEqual(cm.shape, (3, 3))
        self.assertEqual(cm.sum(), 4)


class TestDatasets(unittest.TestCase):
    def test_split_sizes(self):
        X = np.zeros((100, 2))
        y = np.zeros(100)
        Xtr, Xte, ytr, yte = datasets.train_test_split(
            X, y, test_size=0.2, random_state=0
        )
        self.assertEqual(len(Xte), 20)
        self.assertEqual(len(Xtr), 80)

    def test_split_is_deterministic(self):
        X = np.arange(50).reshape(-1, 1)
        y = np.arange(50)
        first = datasets.train_test_split(X, y, random_state=9)
        second = datasets.train_test_split(X, y, random_state=9)
        for a, b in zip(first, second):
            np.testing.assert_array_equal(a, b)


if __name__ == "__main__":
    unittest.main(verbosity=2)
