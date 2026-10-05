# Smoggbot

> Classic machine learning algorithms implemented **from scratch in NumPy** — no scikit-learn, no shortcuts.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![NumPy](https://img.shields.io/badge/numpy-%3E%3D1.24-orange)
![Tests](https://img.shields.io/badge/tests-14%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Smoggbot is a personal academic project that rebuilds foundational ML algorithms
by hand to show how they actually work under the hood. Every estimator is written
with plain NumPy, documented with its underlying maths, and covered by unit tests.

## ✨ Features

- **Linear Regression** — ordinary least squares via the closed-form normal equation
- **k-Nearest Neighbours** — classifier with vectorised Euclidean distances and majority vote (+ `predict_proba`)
- **k-Means Clustering** — Lloyd's algorithm with seeded random initialisation and empty-cluster handling
- **Metrics** — accuracy, precision, recall, F1, confusion matrix, MSE, R²
- **Datasets** — synthetic data generators (regression, classification blobs) and a seeded train/test splitter
- **Tested** — 14 unit tests using only the standard library (`unittest`)

## 📁 Project structure
