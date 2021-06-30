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