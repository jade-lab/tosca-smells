import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import scipy.stats as stats

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import RobustScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor

metrics = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

print(metrics.shape)
# 1. Remove duplicates
metrics.drop_duplicates(subset=metrics.columns.difference(['url']), inplace=True)
print(metrics.shape)

X = metrics.drop(['url'], axis=1)

# 2. Remove correlated variables (i.e., features for which VIF > 10)
while True:
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

    if any([vif > 10 for vif in vif_data.VIF]):
        # Remove feature with the highest VIF
        idx = vif_data[['VIF']].idxmax().iloc[0]
        print(f'Removing {vif_data.iloc[idx].feature} (VIF > 10)')
        X.drop(vif_data.iloc[idx].feature, axis=1, inplace=True)
    else:
        break

print(f'\nThe following columns are retained: {" ".join(X.columns.to_list())}')

# 3. Normalize data
columns = X.columns
scaler = RobustScaler()
X = pd.DataFrame(scaler.fit_transform(X), columns=columns)

# 4. Clustering
N_CLUSTERS = 2
kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42)
cluster_labels = kmeans.fit_predict(X)

# The silhouette_score gives the average value for all the samples.
# This gives a perspective into the density and separation of the formed clusters
silhouette_avg = silhouette_score(X, cluster_labels)
print("\nFor n_clusters =", N_CLUSTERS,
      "The average silhouette_score is :", silhouette_avg)

# ==================== UNCOMMENT SECTION BELOW AND CHANGE feature1 AND feature2 TO PLOT CLUSTERS =======================
# Create a subplot with 1 row and 2 columns
# fig, ax = plt.subplots()
# fig.set_size_inches(18, 10)
#
# # Plot showing the actual clusters formed
# colors = cm.nipy_spectral(cluster_labels.astype(float) / N_CLUSTERS)
#
# feature1 = 'lines_code'
# feature2 = 'num_interfaces'
# ax.scatter(X[feature1], X[feature2], marker='.', s=70, lw=0, alpha=1, c=colors, edgecolor='k')
#
# # Labeling the clusters
# centers = kmeans.cluster_centers_
#
# # Draw white circles at cluster centers
# ax.scatter(centers[:, 0], centers[:, 1], marker='o', c="white", alpha=1, s=200, edgecolor='k')
#
# for i, c in enumerate(centers):
#     ax.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=25, edgecolor='k')
#
# ax.set_title("The visualization of the clustered data.")
# ax.set_xlabel(f'Feature space for {feature1}')
# ax.set_ylabel(f'Feature space for {feature2}')
#
# plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
#               "with n_clusters = %d" % N_CLUSTERS),
#              fontsize=14, fontweight='bold')
#
# plt.show()
# ===================================================== END TMP =====================================================


# 5. Label clusters
X['url'] = metrics.url.to_list()
clusters = {}

# Create an empty DataFrame for each cluster
for idx in set(cluster_labels):
    clusters[idx] = pd.DataFrame()

for i in range(len(cluster_labels)):
    cluster_id = cluster_labels[i]
    clusters[cluster_id] = clusters[cluster_id].append(X.iloc[i])

# Compute the Sum of Feature values of each Module for each cluster
# and store its average
asfm = {}
for id, cluster in clusters.items():
    asfm[id] = np.mean(cluster.sum(axis=1))

id_highest_asfm = max(asfm, key=asfm.get)

for id, cluster in clusters.items():
    urls = cluster.url.to_list()
    cluster.drop(['url'], axis=1, inplace=True)

    # Transforming back to original metric value
    columns = cluster.columns
    clusters[id] = pd.DataFrame(scaler.inverse_transform(cluster), columns=columns)

    clusters[id]["cluster_id"] = id
    clusters[id]["url"] = urls

    if id == id_highest_asfm:
        clusters[id]["smelly"] = True
    else:
        clusters[id]["smelly"] = False

# Merge and save cluster data
merged_clusters = pd.concat(cluster for cluster in clusters.values())[['cluster_id', 'url', 'smelly']]
merged_clusters.to_csv(os.path.join('data', 'clusters.csv'), index=False)


# 5. Statistical Analysis
def cohen_d(d1, d2):
    # calculate the size of samples
    n1, n2 = len(d1), len(d2)
    # calculate the variance of the samples
    s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
    # calculate the pooled standard deviation
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    # calculate the means of the samples
    u1, u2 = np.mean(d1), np.mean(d2)
    # calculate the effect size
    return (u1 - u2) / s


smelly_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(True) > 0)
sound_cluster = pd.concat(cluster for cluster in clusters.values() if cluster.smelly.to_list().count(False) > 0)

smelly_cluster.drop(['url', 'cluster_id', 'smelly'], axis=1,  inplace=True)
n_tests = len(smelly_cluster.columns)

print('\nResults from Mann-Whitney U test. The metrics below are distributed independently from whether the blueprint '
      'is smelly or not.')

for feature in smelly_cluster.columns:
    group1 = smelly_cluster[feature]
    group2 = sound_cluster[feature]

    u_stat, p_value = stats.mannwhitneyu(group1, group2, alternative='greater')
    d = cohen_d(group1, group2)

    if p_value * n_tests < 0.01:
        print(f'{feature} (corrected p={p_value * n_tests}, U={u_stat}, d={d}, mean smelly: {round(np.mean(group1))}, '
              f'mean sound {int(np.mean(group2))})')

print(f'\nNumber of tests: {n_tests}, corrected p-value: {0.01 / n_tests}')
