import numpy as np
import pandas as pd

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, matthews_corrcoef, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

from create_ml_datasets import large_class_2_metrics, lazy_class_2_metrics, long_method_2_metrics


def print_performance(y_true, y_pred):
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    print('\tPrecision:', round(precision * 100, 2))
    print('\tRecall:', round(recall * 100, 2))


def clustering(X_test, y_test, method: str='k-means'):
    num_clusters = 2

    clustering = KMeans(n_clusters=num_clusters, random_state=0)

    if method == 'agglomerative':
        clustering = AgglomerativeClustering(n_clusters=num_clusters)

    predictions = clustering.fit_predict(X_test)

    X_test = pd.DataFrame(X_test)
    X_test['smelly'] = y_test

    clusters = {}

    # Create an empty DataFrame for each cluster
    for idx in set(predictions):
        clusters[idx] = pd.DataFrame()

    for i in range(len(predictions)):
        cluster_id = predictions[i]
        clusters[cluster_id] = clusters[cluster_id].append(X_test.iloc[i])

    asfm = []  # Average Sum of Feature values of each Module

    # Compute the SFM for each cluster
    for _, cluster in clusters.items():
        cluster["sfm"] = cluster.drop('smelly', axis=1).sum(axis=1)
        asfm.append(cluster["sfm"].mean())

    # Compute the Mean of SFM
    masfm = np.mean(asfm)

    y_pred = []
    y_true = []

    for _, cluster in clusters.items():
        cluster["prediction"] = 1 if cluster["sfm"].mean() >= masfm else 0

        y_pred.extend(cluster.prediction)
        y_true.extend(cluster.smelly)

    print_performance(y_true, y_pred)


def main():
    min_max = MinMaxScaler()
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for smell in ('large_class', 'lazy_class', 'long_method'):

        print(f'Building and evaluating models for: {smell}')

        if smell == 'large_class':
            df = large_class_2_metrics()
        elif smell == 'lazy_class':
            df = lazy_class_2_metrics()
        else:
            df = long_method_2_metrics()

        X = df.drop(['smelly'], axis=1).fillna(0)
        y = df.smelly.ravel()

        dummy_clf = DummyClassifier(strategy='constant', constant=1)
        tree_clf = DecisionTreeClassifier()

        k = 0
        for train_index, test_index in skf.split(X, y):
            print(f'***** Fold: {k}')
            k += 1

            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y[train_index], y[test_index]

            # Scale observations in range [0,1]
            X_train_norm = min_max.fit_transform(X_train)
            X_test_norm = min_max.transform(X_test)

            # Dummy classifier
            dummy_clf.fit(X_train_norm, y_train)
            y_pred = dummy_clf.predict(X_test_norm)
            print('\nDummy classifier')
            print_performance(y_test, y_pred)

            # Decision Tree classifier
            tree_clf.fit(X_train_norm, y_train)
            y_pred = tree_clf.predict(X_test_norm)
            print('\nDecision Tree classifier')
            print_performance(y_test, y_pred)

            # Clustering
            print('\nK-means')
            clustering(X_test_norm, y_test, method='k-means')
            print()


main()
