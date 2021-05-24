import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture


def smell_clustering(X_test: pd.DataFrame, feature_columns: list, smell: str):

    # Sum for label determination
    X_test["metrics_sum"] = X_test.loc[:, feature_columns].sum(axis=1)

    # Aglo
    agglo_model = AgglomerativeClustering(n_clusters=2)
    X_test["agglo_labels"] = agglo_model.fit_predict(X_test[feature_columns])

    # GM
    gm_model = GaussianMixture(n_components=2)
    X_test["gm_labels"] = gm_model.fit_predict(X_test[feature_columns])

    # Kmeans
    kmeans_model = KMeans(n_clusters=2)
    X_test["kmeans_labels"] = kmeans_model.fit_predict(X_test[feature_columns])

    # assign with cluster is smelly or not
    X_test = label_determination(
        X_test, feature_columns, "agglo_labels", smell)
    X_test = label_determination(X_test, feature_columns, "gm_labels", smell)
    X_test = label_determination(
        X_test, feature_columns, "kmeans_labels", smell)

    return X_test[["agglo_labels", "gm_labels", "kmeans_labels"]]


def label_determination(df, feature_columns, label_column, smell):

    label_zero_average = df[df[label_column] == 0]["metrics_sum"].mean()
    label_one_average = df[df[label_column] == 1]["metrics_sum"].mean()
    print("label zero: ", label_zero_average)
    print("label one: ", label_one_average)

    if (
        smell == "large_class" or smell == "long_method"
    ) and label_zero_average > label_one_average:
        df[label_column] = np.where((df[label_column] == 0), 1, 0)

    elif (
        smell == "large_class" or smell == "long_method"
    ) and label_zero_average < label_one_average:
        df[label_column] = np.where((df[label_column] == 1), 1, 0)

    elif smell == "lazy_class" and label_zero_average > label_one_average:
        df[label_column] = np.where((df[label_column] == 1), 1, 0)

    elif smell == "lazy_class" and label_zero_average < label_one_average:
        df[label_column] = np.where((df[label_column] == 0), 1, 0)
    else:
        df[label_column] = "equal"

    return df
