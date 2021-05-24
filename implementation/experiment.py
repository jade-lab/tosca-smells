import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import matthews_corrcoef, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import MinMaxScaler

min_max = MinMaxScaler()
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


def print_performance(y_true, y_pred):
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    print('Precision:', round(precision * 100, 2), 'Recall:', round(recall * 100, 2))


for path_to_csv in ('implementation/large_class_metrics.csv',):
    df = pd.read_csv(path_to_csv)

    if 'type' in df.columns:
        df.drop(['type'], axis=1, inplace=True)
    if 'url' in df.columns:
        df.drop(['type'], axis=1, inplace=True)

    X = df.drop(['smelly'], axis=1).fillna(0)
    y = df.smelly.ravel()
    dummy_clf = DummyClassifier(strategy='constant', constant='1')
    tree_clf = DecisionTreeClassifier()

    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y[train_index], y[test_index]

        # Scale observations in range [0,1]
        X_train_norm = min_max.fit_transform(X_train)
        X_test_norm = min_max.transform(X_test)

        # DummyClassifier
        dummy_clf.fit(X_train_norm, y_train)
        y_pred = dummy_clf.predict(X_test_norm)
        print('Dummy classifier')
        print_performance(y_test, y_pred)

        # DecisionTree
        tree_clf.fit(X_train_norm, y_train)
        y_pred = tree_clf.predict(X_test_norm)
        print('Decision Tree classifier')
        print_performance(y_test, y_pred)

        print()

    break

