"""smoggbot: machine learning algorithms implemented from scratch with NumPy.

Modules:
    linear_regression: Ordinary least squares linear regression.
    knn:               k-Nearest Neighbours classifier.
    kmeans:            k-Means clustering.
    metrics:           Evaluation metrics for classification and regression.
    datasets:          Synthetic dataset generators and train/test splitting.
"""

from .linear_regression import LinearRegression
from .knn import KNNClassifier
from .kmeans import KMeans
from . import metrics, datasets

__all__ = ["LinearRegression", "KNNClassifier", "KMeans", "metrics", "datasets"]
__version__ = "1.0.0"
