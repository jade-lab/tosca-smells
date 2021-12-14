import os
import pandas as pd

import numpy as np


from clustering import core
from sklearn.decomposition import PCA

metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

# Prepare data
X = metrics_df.drop(['url'], axis=1)

# Remove correlated variables (i.e., features for which VIF > 10)
core.reduce_multicollinearity(X)

# Normalize dataset
_, X = core.normalize(X)

thresholds = dict()

# calculate threshold for every metrics
for metric in X.columns:
    q1, q3 = np.percentile(X[metric], [25, 75])
    iqr = q3 - q1
    thresholds[metric] = round(q3 + (1.5*iqr), 2)

for idx, row in X.iterrows():

    smelly_and = True
    smelly_or = False

    for metric, threshold in thresholds.items():

        if row[metric] > threshold:
            smelly_or = True
        else:
            smelly_and = False

    X.loc[idx, 'smelly_and'] = smelly_and
    X.loc[idx, 'smelly_or'] = smelly_or


if X.smelly_and.to_list().count(True) > 0:
    metrics_df['smelly'] = X.smelly_and
    print('Performance using the LOGIC AND rule')
    core.calculate_performance(metrics_df)

if X.smelly_or.to_list().count(True) > 0:
    metrics_df['smelly'] = X.smelly_or
    print('Performance using the LOGIC OR rule')
    core.calculate_performance(metrics_df)

