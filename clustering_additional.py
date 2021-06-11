import os
import numpy as np
import pandas as pd
import core

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# Load data
metrics = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

# Remove duplicates
metrics.drop_duplicates(subset=metrics.columns.difference(['url']), inplace=True)

# Prepare data
X = metrics.drop(['url'], axis=1)

# Remove correlated variables (i.e., features for which VIF > 10)
core.reduce_multicollinearity(X)

# Normalize dataset dividing observations for lines of code
X = metrics.drop(['url'], axis=1)
X = X.div(X.lines_code, axis=0)
X = X.drop(['lines_code'], axis=1)

# Cluster data with KMeans
N_CLUSTERS = 2
cluster_labels = KMeans(n_clusters=N_CLUSTERS, random_state=42).fit_predict(X)
print("\n[CLUSTERING] The average silhouette score for KMeans is :", silhouette_score(X, cluster_labels))

# Label according to the labeled schema described in Section 3.3
X['url'] = metrics.url.to_list()
clusters = {}

# Create an empty DataFrame for each cluster label (0 and 1)
for idx in set(cluster_labels):
    clusters[idx] = pd.DataFrame()

for i in range(len(cluster_labels)):
    cluster_id = cluster_labels[i]
    clusters[cluster_id] = clusters[cluster_id].append(X.iloc[i])

# Compute the Sum of Feature values for each cluster and store its average
asfm = {}
for id, cluster in clusters.items():
    asfm[id] = np.mean(cluster.sum(axis=1))

id_highest_asfm = max(asfm, key=asfm.get)

for cluster_id, cluster_df in clusters.items():
    clusters[cluster_id]["cluster_id"] = cluster_id

    if cluster_id == id_highest_asfm:
        clusters[cluster_id]["smelly"] = True
    else:
        clusters[cluster_id]["smelly"] = False

# Merge smelly and sound clusters and save to disk
merged_clusters = pd.concat(cluster for cluster in clusters.values())[['cluster_id', 'url', 'smelly']]
merged_clusters.to_csv(os.path.join('data', 'clusters.csv'), index=False)

# Statistical Analysis
smelly_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(True) > 0)
sound_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(False) > 0)
core.statistical_analysis(smelly_cluster, sound_cluster)

# Performance
core.calculate_performance(merged_clusters)
