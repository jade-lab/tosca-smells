import os
import numpy as np
import pandas as pd
from clustering import core

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score


def main(method='kmeans'):
    # Load data
    metrics = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

    # Remove duplicates
    metrics.drop_duplicates(subset=metrics.columns.difference(['url']), inplace=True)

    # Prepare data
    X = metrics.drop(['url'], axis=1)

    # Remove correlated variables (i.e., features for which VIF > 10)
    core.reduce_multicollinearity(X)

    # Normalize dataset
    normalizer, X = core.normalize(X)

    # Cluster data with KMeans
    N_CLUSTERS = 2

    if method == 'kmeans':
        cluster_labels = KMeans(n_clusters=N_CLUSTERS, random_state=42).fit_predict(X)
    else:  # method == 'agglomerative':
        cluster_labels = AgglomerativeClustering(n_clusters=N_CLUSTERS).fit_predict(X)

    print(f"\n[CLUSTERING] The average silhouette score for {method} is :", silhouette_score(X, cluster_labels))

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

        # Temporary removing URLS to avoid errors when performing the inverse_transform below
        urls = cluster_df.url.to_list()
        cluster_df.drop(['url'], axis=1, inplace=True)

        # Transforming back to original metric values
        columns = cluster_df.columns
        clusters[cluster_id] = pd.DataFrame(normalizer.inverse_transform(cluster_df), columns=columns)

        clusters[cluster_id]["cluster_id"] = cluster_id
        clusters[cluster_id]["url"] = urls

        if cluster_id == id_highest_asfm:
            clusters[cluster_id]["smelly"] = True
        else:
            clusters[cluster_id]["smelly"] = False

    # Merge smelly and sound clusters and save to disk
    merged_clusters = pd.concat(cluster for cluster in clusters.values())[['cluster_id', 'url', 'smelly']]
    merged_clusters.to_csv(os.path.join('data', f'clusters_{method}.csv'), index=False)

    # Statistical Analysis
    smelly_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(True) > 0)
    sound_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(False) > 0)
    core.statistical_analysis(smelly_cluster, sound_cluster)

    # Performance
    core.calculate_performance(merged_clusters)
