import numpy as np
import pandas as pd

from .experiment import AbstractExperiment
from sklearn.cluster import AgglomerativeClustering, MiniBatchKMeans, KMeans
from sklearn.metrics import silhouette_score


class ClusteringExperiment(AbstractExperiment):

    def __init__(self, n_repeats: int = 100, method: str = 'kmeans'):
        super(self.__class__, self).__init__(n_repeats)
        self.method = method

    def detect_smells(self, dataset):

        best_n = (0, 0, [])  # (n, silhouette_score, cluster_labels)

        for n in range(2, 10):

            if self.method == 'kmeans':
                cluster_labels = KMeans(n_clusters=n, random_state=42).fit_predict(dataset)
            elif self.method == 'mini-batch':
                cluster_labels = MiniBatchKMeans(n_clusters=n, random_state=42).fit_predict(dataset)
            elif self.method == 'agglomerative':
                cluster_labels = AgglomerativeClustering(n_clusters=n).fit_predict(dataset)
            else:
                return

            score = silhouette_score(dataset, cluster_labels)
            if score > best_n[1]:
                best_n = (n, score, cluster_labels)

        print('n:', best_n[0], 'Silhouette:', best_n[1])

        # Label according to the labeled schema described in the Methodology
        cluster_labels = best_n[2]
        clusters = {}

        # Create entries in the dictionary "clusters" where the key is the cluster label (e.g., 0, 1, 2, etc.) and the
        # value is an empty DataFrame to be populated later
        for idx in set(cluster_labels):
            clusters[idx] = pd.DataFrame()

        # Populate clusters
        for i in range(len(cluster_labels)):
            label = cluster_labels[i]
            clusters[label] = clusters[label].append(dataset.iloc[i])

        # Compute the Sum of Feature values for each cluster and store its average
        asfm = {}
        for label, cluster_df in clusters.items():
            asfm[label] = np.mean(cluster_df.sum(axis=1))

        # Calculate the median ASFM that is used as a threshold above which clusters are classified as smelly
        median_asfm = np.median(list(asfm.values()))

        # Label clusters as smelly or not
        for label, cluster_df in clusters.items():
            is_smelly = False

            if asfm[label] > median_asfm:
                is_smelly = True

            for idx, _ in cluster_df.iterrows():
                yield idx, is_smelly
