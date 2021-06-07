import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


from sklearn.metrics import make_scorer, matthews_corrcoef, average_precision_score, precision_recall_curve, roc_curve, \
    auc, PrecisionRecallDisplay, precision_score, roc_curve, plot_roc_curve
from sklearn.model_selection import RepeatedKFold, RepeatedStratifiedKFold, StratifiedKFold, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.feature_selection import SelectKBest, chi2, VarianceThreshold
from pyod.utils.utility import standardizer
import matplotlib.pyplot as plt
from pyod.models.knn import KNN
from pyod.models.combination import average, maximization, aom, moa
from sklearn.pipeline import Pipeline
from pyod.models.iforest import IForest
from pyod.models.pca import PCA

settings = {
    'knn': {
        'estimator': KNN(),
        'search_params': {
            'estimator__n_neighbors': np.linspace(1, 51, 10, dtype=np.int32),
            'estimator__contamination': np.linspace(0.01, 0.5, 100),
            'estimator__method': ['largest', 'mean', 'median']
        }
    },
    'iforest': {
        'estimator': IForest(random_state=42),
        'search_params': {
            'estimator__n_estimators': np.linspace(1, 51, 10, dtype=np.int32),
            'estimator__contamination': np.linspace(0.001, 0.5, 100),
        }
    },
    'pca': {
        'estimator': PCA(random_state=42),
        'search_params': {
            'estimator__n_components': np.linspace(1, 16, 8, dtype=np.int32),
            'estimator__n_selected_components': np.linspace(1, 16, 8, dtype=np.int32),
            'estimator__contamination': np.linspace(0.001, 0.5, 100),
        }
    }
}


for smell in ('lazy_class',):
    print(f'Building and evaluating models for: {smell}')

    df = pd.read_csv(f'implementation/metrics/{smell}.csv').fillna(0)
    df.drop_duplicates(inplace=True)

    X = VarianceThreshold().fit_transform(df.drop(['smelly'], axis=1))
    y = df.smelly.ravel()

    for detector in ('iforest', 'knn', 'pca',):

        print('Building and evaluating:', detector)

        pipe = Pipeline([
            ('preprocessing', StandardScaler()),
            ('estimator', settings[detector]['estimator'])
        ])

        search = RandomizedSearchCV(pipe, settings[detector]['search_params'],
                                    cv=RepeatedStratifiedKFold(n_splits=2, n_repeats=2, random_state=42).split(X, y),
                                    scoring='average_precision', refit='average_precision', error_score=0, verbose=0)
        search.fit(X, y)

        # Take only the scores at the best index and save file
        performance = pd.DataFrame(search.cv_results_).iloc[[search.best_index_]]
        performance.to_csv(f'{detector}.csv', index=False)

        best_estimator = search.best_estimator_.named_steps['estimator']

        y_true = []
        test_scores = []
        for idx_train, idx_test in RepeatedStratifiedKFold(n_splits=2, n_repeats=2, random_state=42).split(X, y):
            X_train, X_test = X[idx_train], X[idx_test]
            best_estimator.fit(X_train)

            y_true.extend(y[idx_test])
            test_scores.extend(best_estimator.decision_function(X_test))

        precision, recall, _ = precision_recall_curve(y_true, test_scores, pos_label=1)
        fig, ax = plt.subplots()
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.plot(recall, precision, label='Overall AUC=%.4f' % (auc(recall, precision)), color='black')
        ax.legend()
        plt.show()

        tpr, fpr, _ = roc_curve(y_true, test_scores)
        fig, ax = plt.subplots()
        ax.set_xlabel('fpr')
        ax.set_ylabel('tpr')
        ax.plot(fpr, tpr, label='Overall AUC=%.4f' % (auc(fpr, tpr)), color='black')
        ax.legend()
        plt.show()


            # y_true = []
            # test_scores = np.zeros([X_test.shape[0], len(k_list)])
            #
            # for i in range(10):
            #     k = k_list[i]
            #     clf = KNN(n_neighbors=random.choice(k_list),
            #               method=random.choice(method_list),
            #               contamination=random.choice(contamination_list))
            #
            #     clf.fit(X_train)
            #     test_scores[:, i] = clf.decision_function(X_test)
            #
            # y_true.extend(y_test)
            # test_scores_norm = standardizer(test_scores)
            # comb_by_average = average(test_scores_norm)
            # comb_by_maximization = maximization(test_scores_norm)
            # comb_by_aom = aom(test_scores_norm, 5) # 5 groups
            # comb_by_moa = moa(test_scores_norm, 5) # 5 groups

            # precision, recall, _ = precision_recall_curve(y_true, comb_by_moa, pos_label=1)
            # fig, ax = plt.subplots()
            # ax.set_xlabel('Recall')
            # ax.set_ylabel('Precision')
            # ax.plot(recall, precision, label='Overall AUC=%.4f' % (auc(recall, precision)), color='black')
            # ax.legend()
            # plt.show()

        # train kNN detector
        # clf = KNN(contamination=0.21, n_neighbors=12)
        # clf.fit(X_train)
        #
        # # get the prediction on the test data
        # y_test_scores = clf.decision_function(X_test)  # outlier scores
        # y_true.extend(y_test)
        # y_scores.extend(y_test_scores)

    # precision, recall, _ = precision_recall_curve(y_true, y_scores, pos_label=1)
    # fig, ax = plt.subplots()
    # ax.set_xlabel('Recall')
    # ax.set_ylabel('Precision')
    # ax.plot(recall, precision, label='Overall AUC=%.4f' % (auc(recall, precision)), color='black')
    # ax.legend()
    # plt.show()
