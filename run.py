import os
import numpy as np
import pandas as pd
import random

from clustering import core
from scipy.stats import chi2


def iqr_strategy(X: pd.DataFrame):
    thresholds = dict()

    # calculate threshold for every metrics
    for metric in X.columns:
        q1, q3 = np.percentile(X[metric], [25, 75])
        iqr = q3 - q1
        thresholds[metric] = round(q3 + (1.5 * iqr), 2)

    for idx, row in X.iterrows():

        X.loc[idx, 'smelly'] = False

        for metric, threshold in thresholds.items():

            if row[metric] > threshold:
                X.loc[idx, 'smelly'] = True
                break


def mahalanobis_strategy(X: pd.DataFrame):
    def mahalanobis(x=None, data=None, cov=None):
        x_mu = x - np.mean(data)
        if not cov:
            cov = np.cov(data.values.T)
        inv_covmat = np.linalg.inv(cov)
        left = np.dot(x_mu, inv_covmat)
        mahal = np.dot(left, x_mu.T)
        return mahal.diagonal()

    # create new column in dataframe that contains Mahalanobis distances for each row
    X['mahalanobis'] = mahalanobis(x=X, data=X[X.columns])

    # calculate p-value for each mahalanobis distance
    X['p'] = 1 - chi2.cdf(X['mahalanobis'], X.shape[1] - 2)

    for idx, row in X.iterrows():
        X.loc[idx, 'smelly'] = row['p'] < 0.01


metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)
num_observations = []
mcc_iqr = []
mcc_mah = []
precision_iqr = []
precision_mah = []
recall_iqr = []
recall_mah = []

random.seed(42)

for i in range(0, 100):
    metrics_subset_df = metrics_df.sample(n=random.randint(100, metrics_df.shape[0]), random_state=42)
    num_observations.append(metrics_subset_df.shape[0])
    print('Iteration:', i, 'Num observations:', metrics_subset_df.shape[0])

    # Prepare data
    X = metrics_subset_df.drop(['url'], axis=1)

    # Remove correlated variables (i.e., features for which VIF > 10)
    core.reduce_multicollinearity(X, print_result=False)

    # Normalize dataset
    _, X = core.normalize(X)

    X_iqr = X.copy()
    X_mah = X.copy()

    iqr_strategy(X_iqr)
    evaluation = core.calculate_performance(metrics_subset_df.assign(smelly=X_iqr.smelly.to_list()), print_result=False)
    mcc_iqr.append(evaluation['mcc'])
    precision_iqr.append(evaluation['precision'])
    recall_iqr.append(evaluation['recall'])

    mahalanobis_strategy(X_mah)
    evaluation = core.calculate_performance(metrics_subset_df.assign(smelly=X_mah.smelly.to_list()), print_result=False)
    mcc_mah.append(evaluation['mcc'])
    precision_mah.append(evaluation['precision'])
    recall_mah.append(evaluation['recall'])

print(f'Median number of observations per set: {np.median(num_observations)}\n' +
      '================== IQR ==================\n' +
      f'Median MCC: {np.median(mcc_iqr)}\n' +
      f'Median precision: {np.median(precision_iqr)}\n' +
      f'Median recall: {np.median(recall_iqr)}\n' +
      '================== MHA ==================\n' +
      f'Median MCC: {np.median(mcc_mah)}\n' +
      f'Median precision: {np.median(precision_mah)}\n' +
      f'Median recall: {np.median(recall_mah)}')