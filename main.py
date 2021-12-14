from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment
from experiments.threshold import StaticThresholdExperiment

print('Enter:\n- 1 to reproduce the experiment using the Mahalanobis distance.\n- 2 to reproduce the experiment '
      'using the IQR rule.\n- 3 to reproduce the experiment using KMeans.\n- 4 to '
      'reproduce the experiment using AgglomerativeClustering.\nChoice:', end=' ')
value = input()

if value == '1':
    experiment = MahalanobisExperiment(n_repeats=10)
    experiment.run()
    experiment.print_performance()
elif value == '2':
    experiment = IQRExperiment(n_repeats=100)
    experiment.run()
    experiment.print_performance()
if value == '3':
    experiment = ClusteringExperiment(n_repeats=100, method='kmeans')
    experiment.run()
    experiment.print_performance()
if value == '4':
    experiment = ClusteringExperiment(n_repeats=100, method='agglomerative')
    experiment.run()
    experiment.print_performance()
if value == '5':
    experiment = ClusteringExperiment(n_repeats=100, method='spectral')
    experiment.run()
    experiment.print_performance()
if value == '9':
    experiment = StaticThresholdExperiment(n_repeats=100)
    experiment.run()
    experiment.print_performance()
else:
    exit(0)



exit()

# EXAMPLE OF USAGE:
# python main.py {1, 2, 3, 4} {kmeans, agglomerative}

import sys
from clustering import clustering, clustering_additional, clustering_loc, clustering_significant_metrics

# EXPERIMENT options:
# 1 - Build and evaluate clustering using all metrics
# 2 - Build and evaluate clustering using all metrics normalized by the lines of code
# 3 - Build and evaluate clustering using the metric 'lines of code' only
# 4 - Build and evaluate clustering using only the metrics deemed 'significant' by the Mann-Withney U test in 1.
EXPERIMENT = sys.argv[1]

# ALGORITHM options:
# kmeans - Build and evaluate clustering using KMeans
# agglomerative - Build and evaluate clustering using AgglomerativeClustering
ALGORITHM = sys.argv[2]

if EXPERIMENT == '1':
    clustering.main(ALGORITHM)
elif EXPERIMENT == '2':
    clustering_additional.main(ALGORITHM)
elif EXPERIMENT == '3':
    clustering_loc.main(ALGORITHM)
elif EXPERIMENT == '4':
    clustering_significant_metrics.main(ALGORITHM)