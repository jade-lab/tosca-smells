import numpy as np
import pandas as pd



from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE

from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, average_precision_score, matthews_corrcoef, accuracy_score, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV, RepeatedStratifiedKFold, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from imblearn.pipeline import Pipeline

scoring = dict(
    roc_auc='roc_auc',
    pr_auc='average_precision',
    accuracy='accuracy',
    balanced_accuracy='balanced_accuracy',
    precision='precision',
    recall='recall',
    f1='f1'
)


def train():
    df = pd.read_csv('implementation/metrics/large_class.csv')
    X = df.drop(['smelly'], axis=1).fillna(0)
    y = df.smelly.ravel()

    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)

    _search_params = dict(
        clf__n_estimators=[int(x) for x in np.linspace(start=100, stop=2000, num=10)],
        clf__max_features=['auto', 'sqrt'],
        clf__max_depth=max_depth,
        clf__bootstrap=[True, False]
    )

    _search_params['bal'] = [None, RandomUnderSampler(sampling_strategy='majority', random_state=42),
                             RandomOverSampler(sampling_strategy='minority', random_state=42)]
    _search_params['pre'] = [None, MinMaxScaler(), StandardScaler()]

    pipe = Pipeline([
        ('bal', None),  # To balance the training data See search_params['bal']
        ('pre', None),  # To scale (and center) data. See search_params['pre']
        ('clf', RandomForestClassifier())
    ])

    search = RandomizedSearchCV(pipe, _search_params, cv=10, scoring=scoring, refit='pr_auc', verbose=3)
    search.fit(X, y)

    print()
    performance = pd.DataFrame(search.cv_results_).iloc[[search.best_index_]]
    print(performance)

train()