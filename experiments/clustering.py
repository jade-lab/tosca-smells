import random

import numpy as np
import pandas as pd

from .experiment import AbstractExperiment
from sklearn.cluster import AgglomerativeClustering, KMeans, SpectralClustering
from sklearn.metrics import silhouette_score

RANDOM_STATE = 42


class ClusteringExperiment(AbstractExperiment):

    def __init__(self, n_repeats: int = 100, method: str = 'kmeans'):
        """

        Parameters
        ----------
        n_repeats : int
            Number of times the experiment needs to be repeated for validation.

        method : string
            The clustering technique to use.

            Options
            -------
            - 'affinity' : AffinityPropagation
            - 'agglomerative' : AgglomerativeClustering
            - 'kmeans' : KMeans
            - 'meanshift' : MeanShift
            - 'spectral' : SpectralClustering
            - 'dbscan' : DBSCAN
            - 'birch' : BIRCH
        """
        super(self.__class__, self).__init__(n_repeats)
        self.method = method

    def detect_smells(self, dataset):

        if self.method == 'agglomerative':
            cluster_labels = agglomerative_clustering_random_search(dataset)
        elif self.method == 'kmeans':
            cluster_labels = kmeans_random_search(dataset)
        elif self.method == 'spectral':
            cluster_labels = spectral_clustering_random_search(dataset)
        else:
            raise ValueError()

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

            if asfm[label] >= median_asfm:
                is_smelly = True

            for idx, _ in cluster_df.iterrows():
                yield idx, is_smelly


def agglomerative_clustering_random_search(dataset):
    best_configuration = (None, {}, 0)  # (cluster_labels, parameters, silhouette_score)

    for i in range(0, 10):
        n_clusters = random.randint(2, 20)
        affinity = random.choice(['euclidean', 'l1', 'l2', 'manhattan', 'cosine'])
        linkage = random.choice(['complete', 'average', 'single'])

        cluster_labels = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity, linkage=linkage).fit_predict(
            dataset)

        score = silhouette_score(dataset, cluster_labels)
        if score > best_configuration[2]:
            best_configuration = (cluster_labels,
                                  dict(n_clusters=n_clusters,
                                       affinity=affinity,
                                       linkage=linkage),
                                  score)

    return best_configuration[0]


def kmeans_random_search(dataset):
    best_configuration = (None, {}, 0)  # (cluster_labels, parameters, silhouette_score)

    for i in range(0, 10):
        n_clusters = random.randint(2, 20)
        init = random.choice(['k-means++', 'random'])
        n_init = random.randint(1, 20)
        algorithm = random.choice(['auto', 'full', 'elkan'])

        cluster_labels = KMeans(n_clusters=n_clusters, init=init, n_init=n_init, algorithm=algorithm,
                                random_state=RANDOM_STATE).fit_predict(dataset)

        score = silhouette_score(dataset, cluster_labels)
        if score > best_configuration[2]:
            best_configuration = (cluster_labels,
                                  dict(n_clusters=n_clusters,
                                       init=init,
                                       n_init=n_init,
                                       algorithm=algorithm),
                                  score)

    return best_configuration[0]


def spectral_clustering_random_search(dataset):
    best_configuration = (None, {}, 0)  # (cluster_labels, parameters, silhouette_score)

    for i in range(0, 10):
        n_clusters = random.randint(2, 20)
        eigen_solver = random.choice(['arpack', 'lobpcg', 'amg'])
        n_components = random.randint(1, n_clusters)
        n_init = random.randint(1, 20)
        affinity = random.choice(['nearest_neighbors', 'rbf', 'precomputed', 'precomputed_nearest_neighbors'])
        n_neighbors = random.randint(2, 20)
        assign_labels = random.choice(['kmeans', 'discretize'])

        # eigen_solver = eigen_solver,
        # n_components = n_components,
        # n_init = n_init,
        # affinity = affinity,
        # n_neighbors = n_neighbors,
        # assign_labels = assign_labels,

        cluster_labels = SpectralClustering(n_clusters=n_clusters,
                                            random_state=RANDOM_STATE).fit_predict(dataset)

        score = silhouette_score(dataset, cluster_labels)
        if score > best_configuration[2]:
            best_configuration = (cluster_labels,
                                  dict(n_clusters=n_clusters,
                                       eigen_solver=eigen_solver,
                                       n_components=n_components,
                                       n_init=n_init,
                                       affinity=affinity,
                                       n_neighbors=n_neighbors,
                                       assign_labels=assign_labels),
                                  score)

    return best_configuration[0]
