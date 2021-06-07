import os
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


metrics = pd.read_csv(os.path.join('data', 'metrics.csv'))

X = metrics.drop(['url'], axis=1).fillna(0).drop_duplicates()

# Normalize
columns = X.columns
X = pd.DataFrame(StandardScaler().fit_transform(X), columns=columns)

best_config = {
    'clusterer': None,
    'cluster_labels': None,
    'n_clusters': 0,
    'silhouette_avg': -1
}

# Identify best number of clusters based on silhouette score
range_n_clusters = [2, 3, 5, 8, 13, 21, 34, 65]
for n_clusters in range_n_clusters:

    clusterer = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    if silhouette_avg > best_config['silhouette_avg']:
        best_config['clusterer'] = clusterer
        best_config['cluster_labels'] = cluster_labels
        best_config['n_clusters'] = n_clusters
        best_config['silhouette_avg'] = silhouette_avg

print("The number of clusters that maximize the mean silhouette coefficient is", best_config['n_clusters'])

# Create a subplot with 1 row and 2 columns
fig, ax = plt.subplots()
fig.set_size_inches(18, 10)

# Plot showing the actual clusters formed
colors = cm.nipy_spectral(best_config['cluster_labels'].astype(float) / best_config['n_clusters'])

feature1 = 'lines_code'
feature2 = 'num_node_types'
ax.scatter(X[feature1], X[feature2], marker='.', s=70, lw=0, alpha=1, c=colors, edgecolor='k')

# Labeling the clusters
centers = best_config['clusterer'].cluster_centers_

# Draw white circles at cluster centers
ax.scatter(centers[:, 0], centers[:, 1], marker='o', c="white", alpha=1, s=200, edgecolor='k')

for i, c in enumerate(centers):
    ax.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=25, edgecolor='k')

ax.set_title("The visualization of the clustered data.")
ax.set_xlabel(f'Feature space for {feature1}')
ax.set_ylabel(f'Feature space for {feature2}')

plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
              "with n_clusters = %d" % best_config['n_clusters']),
             fontsize=14, fontweight='bold')

plt.show()

X['url'] = metrics.url
clusters = {}

# Create an empty DataFrame for each cluster
for idx in set(best_config['cluster_labels']):
    clusters[idx] = pd.DataFrame()

for i in range(len(best_config['cluster_labels'])):
    cluster_id = best_config['cluster_labels'][i]
    clusters[cluster_id] = clusters[cluster_id].append(X.iloc[i])

asfm = []  # Average Sum of Feature values of each Module

# Compute the SFM for each cluster
for _, cluster in clusters.items():
    cluster["sfm"] = cluster.sum(axis=1)
    asfm.append(cluster["sfm"].mean())

# Compute the Mean of SFM
masfm = np.mean(asfm)

for id, cluster in clusters.items():
    cluster["cluster_id"] = id
    cluster["smelly"] = True if cluster["sfm"].mean() >= masfm else False
    print(cluster["smelly"].to_list().count(True), 'smelly instances in cluster', id)

merged_clusters = pd.concat(cluster for cluster in clusters.values())[['cluster_id', 'url', 'sfm', 'smelly']]
merged_clusters.to_csv(os.path.join('data', 'clusters.csv'), index=False)

# Mann-Whitney U test satistical tests between smelly and sound clusters
import scipy.stats as stats

smelly_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(True) > 0)
sound_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(False) > 0)

print('Performing the Mann–Whitney U test to compare the distribution of a given feature within the set of smelly '
      'blueprints against the set of sound blueprints. The null hypothesis states that the feature is distributed '
      'independently from whether the blueprint is smelly or not. If rejected, it means that the feature is distributed'
      ' differently in each set and thus is a promising candidate as input to detect the smell.')

n_tests = len(smelly_cluster.columns) - 4
for feature in smelly_cluster.columns:
    if feature in ('url', 'sfm', 'cluster_id', 'smelly'):
        continue

    group1 = smelly_cluster[feature]
    group2 = sound_cluster[feature]

    u_stat, p_value = stats.mannwhitneyu(group1, group2, alternative='greater')

    print(f'The probability that \'{feature}\' is distributed independently from whether the blueprint is smelly or not'
          f' is: {p_value*n_tests} (U={u_stat})')


# We used the Bonferroni correction to correct for multiple testing for the 17 features we tested. Therefore, we test
# against the stricter significance level of 0.00059, which corresponds to a non-corrected p ≤ 0.01 for each individual test.
