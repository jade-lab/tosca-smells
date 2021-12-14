import os
import numpy as np
import pandas as pd
import random

from clustering import core
from scipy.stats import chi2


def mahalanobis(x=None, data=None, cov=None):
    x_mu = x - np.mean(data)
    if not cov:
        cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()


metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

num_observations = []
mcc = []
precision = []
recall = []

random.seed(42)

for i in range(0, 10):

    metrics_subset_df = metrics_df.sample(n=random.randint(100, metrics_df.shape[0]), random_state=42)
    num_observations.append(metrics_subset_df.shape[0])
    print('Iteration:', i, 'Num observations:', metrics_subset_df.shape[0])

    # Prepare data
    X = metrics_subset_df.drop(['url'], axis=1)

    # Remove correlated variables (i.e., features for which VIF > 10)
    core.reduce_multicollinearity(X)

    # Normalize dataset
    normalizer, X = core.normalize(X)

    # create new column in dataframe that contains Mahalanobis distances for each row
    X['mahalanobis'] = mahalanobis(x=X, data=X[X.columns])

    # calculate p-value for each mahalanobis distance
    X['p'] = 1 - chi2.cdf(X['mahalanobis'], X.shape[1] - 2)

    for idx, row in X.iterrows():
        X.loc[idx, 'smelly'] = row['p'] < 0.01

    metrics_subset_df = metrics_subset_df.assign(smelly=X.smelly.to_list())
    evaluation = core.calculate_performance(metrics_subset_df)

    mcc.append(evaluation['mcc'])
    precision.append(evaluation['precision'])
    recall.append(evaluation['recall'])

print('Median number of observations per set:', np.median(num_observations))
print('Median MCC:', np.median(mcc))
print('Median precision:', np.median(precision))
print('Median recall:', np.median(recall))
