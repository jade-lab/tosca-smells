import numpy as np
import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.metrics import make_scorer, matthews_corrcoef, average_precision_score, precision_recall_curve, roc_curve, auc, PrecisionRecallDisplay, precision_score
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold, StratifiedKFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.feature_selection import SelectKBest, chi2, VarianceThreshold
from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest

import matplotlib.pyplot as plt
from pyod.models.knn import KNN
from pyod.utils.data import evaluate_print
# from pyod.utils.utility import standardizer
# from pyod.models.combination import aom, moa, average, maximization

scoring = dict(
    average_precision='average_precision',
    precision='precision',
    recall='recall',
    f1='f1',
    mcc=make_scorer(matthews_corrcoef)
)

settings = {
    'knn': {
        'estimator': KNN(),
        'search_params': {
            'estimator__n_neighbors': np.linspace(1, 5, 100, dtype=np.int32),
            'estimator__contamination': np.linspace(0.01, 0.5, 100),
        }
    },
    'local-outlier-factor': {
        'estimator': LocalOutlierFactor(novelty=True),
        'search_params': {
            'estimator__n_neighbors': np.linspace(1, 1000, 100, dtype=np.int32),
            'estimator__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
            'estimator__metric': ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan'],
            'estimator__contamination': np.linspace(0.01, 0.5, 100)
        }
    },
    'isolation-forest': {
        'estimator': IsolationForest(random_state=42),
        'search_params': {
            'estimator__n_estimators': np.linspace(1, 1000, 100, dtype=np.int32),
            'estimator__contamination': np.linspace(0.01, 0.5, 100),
            'estimator__bootstrap': [True, False],
            'estimator__warm_start': [True, False]
        }
    },
    'one-class-svm': {
        'estimator': OneClassSVM(),
        'search_params': {
            'estimator__kernel': ['poly', 'rbf', 'sigmoid'],
            'estimator__tol': np.logspace(-5.0, -2.0, num=10),
            'estimator__gamma': np.linspace(0.01, 100, 10),
            'estimator__nu': np.linspace(0.01, 0.5, 10),
            'estimator__shrinking': [True, False]
        }
    }
}


def main():
    rkf = RepeatedKFold(n_splits=10, n_repeats=5, random_state=42)

    for smell in ('large_class',):
    # for smell in ('lazy_class',):
    # for smell in ('long_method',):
        print(f'Building and evaluating models for: {smell}')

        df = pd.read_csv(f'implementation/metrics/{smell}.csv').fillna(0)
        df.drop_duplicates(inplace=True)

        X_pos = df[df.smelly == 0].drop(['smelly'], axis=1)  # normal (sound) class
        X_neg = df[df.smelly == 1].drop(['smelly'], axis=1)  # anomalous (smelly) class

        # Creating (train, test) tuples of indices for k-folds cross-validation
        # We split the positive class (normal data) as we only want the positive examples in the training set.
        n, m = len(X_pos), len(X_neg)
        splits = ((train, np.concatenate([test, np.arange(n, n + m)], axis=0)) for train, test in rkf.split(X_pos))

        # X = np.concatenate([X_pos, X_neg], axis=0)
        # y = np.concatenate([np.repeat(1.0, len(X_pos)), np.repeat(-1.0, len(X_neg))])

        # ----------  PYOD
        # initialize 20 base detectors for combination
        X = VarianceThreshold().fit_transform(df.drop(['smelly'], axis=1))
        y = df.smelly.ravel()

        # best_contamination = 0
        # best_mean_auc = 0
        #
        # for contamination in [0.01, 0.1, 0.25, 0.5]:

        #
        #     avg_auc = []
        #

        y_true = []
        y_scores = []

        for idx_train, idx_test in rkf.split(X):
            normalizer = MinMaxScaler()

            X_train = normalizer.fit_transform(X[idx_train])
            X_test = normalizer.transform(X[idx_test])

            y_test = y[idx_test]

            # train kNN detector
            clf = KNN(contamination=0.21, n_neighbors=12)
            clf.fit(X_train)

            # get the prediction on the test data
            y_test_scores = clf.decision_function(X_test)  # outlier scores
            y_true.extend(y_test)
            y_scores.extend(y_test_scores)

                # precision, recall, _ = precision_recall_curve(y_test, y_test_scores, pos_label=1)


                # avg_auc.append(average_precision_score(y_test, y_test_scores))
        #
        #     avg_auc = np.mean(avg_auc)
        #     if avg_auc > best_mean_auc:
        #         best_mean_auc = avg_auc
        #         best_contamination = contamination
        #
        # print(best_contamination, best_mean_auc)
        # exit()
        #
        precision, recall, _ = precision_recall_curve(y_true, y_scores, pos_label=1)
        fig, ax = plt.subplots()
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.plot(recall, precision, label='Overall AUC=%.4f' % (auc(recall, precision)), color='black')
        ax.legend()
        plt.show()
        exit()

    # fig.tight_layout()
        # fig.savefig('result.png')
        #
        #



        # -----------

        splits = rkf.split(X)

        # Training and validation
        for estimator in ('knn',):# 'isolation-forest', 'one-class-svm', 'local-outlier-factor'):

            print(f'Evaluating {estimator}...')

            pipe = Pipeline([
                ('preprocessing', StandardScaler()),
                # ('k_best', SelectKBest(chi2)),
                ('estimator', settings[estimator]['estimator'])
            ])

            search_params = settings[estimator]['search_params']
            # search_params['k_best__k'] = np.linspace(1, X.shape[1], 100, dtype=np.int32)
            if estimator == 'knn':
                search_params['estimator__n_neighbors'] = np.linspace(1, X.shape[1], 100, dtype=np.int32)

            search = RandomizedSearchCV(pipe, search_params, cv=splits, scoring=scoring, refit='average_precision',
                                        error_score=0, verbose=5)
            search.fit(X, y)

            # Take only the scores at the best index and save file
            performance = pd.DataFrame(search.cv_results_).iloc[[search.best_index_]]
            performance.to_csv(f'{estimator}.csv', index=False)


main()
