# For each smell:

# 1. Calculate metrics
# - create_ml_dataset.py

# 2. Preprocess data
# - Delete NaN rows
# - Discard features based on too high VIF score
# - MinMaxScaler, or on trainset? But how to do then with test set?

# 3. 10x5 fold cross validation

# 3a. (Threshold tuning)
# - Train thresholds on train fold
# - Predict test fold
# - Calculate performance (Precision, Recall and MCC)

# 3b. (Supvervised)
# - train decision tree on train fold
# - Predict test fold
# - Calculate performance (Precision, Recall and MCC)

# 3c. (unsupervised)
# - cluster algos for test fold
# - label determination
# - Calculate performance (Precision, Recall and MCC)

# 4. store results

import csv

import pandas as pd
from sklearn.metrics import matthews_corrcoef, precision_score, recall_score
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from clustering import smell_clustering
from create_ml_datasets import (large_class_2_metrics, lazy_class_2_metrics,
                                long_method_2_metrics)


def pipeline(smell):

    if smell == "long_method":
        feature_columns = ["lines_code"]
    else:
        feature_columns = [
            "lines_code",
            "num_tokens",
            "entropy",
            "num_interfaces",
            "num_properties"
        ]

    # Create results csv
    with open(f"implementation/{smell}_results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "counter",
                "thr_prec",
                "thr_reca",
                "thr_mcc",
                "sup_prec",
                "sup_reca",
                "sup_mcc",
                "agl_prec",
                "agl_reca",
                "agl_mcc",
                "gmm_prec",
                "gmm_reca",
                "gmm_mcc",
                "kme_prec",
                "kme_reca",
                "kme_mcc",
            ]
        )

    if smell == "large_class":
        df = large_class_2_metrics()
    elif smell == "lazy_class":
        df = lazy_class_2_metrics()
    elif smell == "long_method":
        df = long_method_2_metrics()
    else:
        raise TypeError(
            f"{smell} is not a valid smell use 'large_class', 'lazy_class', or 'long_method'")

    print(df.head())
    print(df.dtypes)
    df = df.dropna(subset=feature_columns)
    # TODO df = exclude VIF features

    # 3. 10x5 fold cross validation AND MinMaxScaler
    X = df[feature_columns]
    y = df["smelly"]

    rkf = RepeatedKFold(n_splits=5, n_repeats=10, random_state=2652124)

    counter = 0

    for train_index, test_index in rkf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        scaler = MinMaxScaler()
        X_train[feature_columns] = scaler.fit_transform(X_train)
        X_test[feature_columns] = scaler.transform(X_test)

        result_row = [counter]

        # TODO 3a. (Threshold tuning)
        # - Train thresholds on train fold
        # - Predict test fold
        # - Calculate performance (Precision, Recall and MCC)
        result_row.extend([0, 0, 0])

        # 3b. (Supvervised)
        clf = DecisionTreeClassifier(random_state=0)
        clf = clf.fit(X_train, y_train)
        supervised_predictions = clf.predict(X_test)
        supervised_predictions = pd.Series(
            data=supervised_predictions, index=X_test.index)
        result_row.extend(performance_metrics(y_test, supervised_predictions))

        # 3c. (unsupervised)
        clustering_df = smell_clustering(X_test, feature_columns, smell)
        result_row.extend(performance_metrics(
            y_test, clustering_df["agglo_labels"]))
        result_row.extend(performance_metrics(
            y_test, clustering_df["gm_labels"]))
        result_row.extend(performance_metrics(
            y_test, clustering_df["kmeans_labels"]))

        # 4. store results
        with open(f"implementation/{smell}_results.csv", 'a') as f:
            csv.writer(f).writerow(result_row)

        counter += 1


def performance_metrics(y_true, y_pred):
    prec = precision_score(y_true, y_pred, average='micro')
    reca = recall_score(y_true, y_pred, average='micro')
    mcc = matthews_corrcoef(y_true, y_pred)
    return [prec, reca, mcc]


# pipeline("large_class")
pipeline("lazy_class")
pipeline("long_method")
