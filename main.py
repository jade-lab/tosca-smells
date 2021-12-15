import os
import numpy as np
import pandas as pd

from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment
from experiments.statistical_analysis import StatisticalAnalysis
from experiments.threshold import StaticThresholdExperiment

print('Enter:\n- 1 to reproduce the experiment using the Mahalanobis distance.\n- 2 to reproduce the experiment '
      'using the IQR rule.\n- 3 to reproduce the experiment using KMeans.\n- 4 to '
      'reproduce the experiment using AgglomerativeClustering.\n- 5 to '
      'reproduce the experiment using SpectralClustering.\nChoice:', end=' ')
value = input()

# For test only
if value == '1':
    experiment = MahalanobisExperiment(n_repeats=100)
    experiment.run()
    print(experiment.performance_df.describe())
elif value == '2':
    experiment = IQRExperiment(n_repeats=100)
    experiment.run()
    print(experiment.performance_df.describe())
elif value == '3':
    experiment = ClusteringExperiment(n_repeats=100, method='kmeans')
    experiment.run()
    print(experiment.performance_df.describe())
elif value == '4':
    experiment = ClusteringExperiment(n_repeats=100, method='agglomerative')
    experiment.run()
    print(experiment.performance_df.describe())
elif value == '5':
    experiment = ClusteringExperiment(n_repeats=100, method='spectral')
    experiment.run()
    print(experiment.performance_df.describe())
elif value == '9':
    experiment = StaticThresholdExperiment(n_repeats=100)
    experiment.run(multicollinearity_reduction=False)
    print(experiment.performance_df.describe())

# =====================================

elif value == '0':
    experiments = dict(
        iqr=IQRExperiment,
        # mahalanobis=MahalanobisExperiment,
        # kmeans=ClusteringExperiment
    )

    best_performing_algorithm = {'class': None, 'algorithm': None, 'median_mcc': -1}

    for algorithm, experiment_class in experiments.items():
        print(f'Running experiment using algorithm={algorithm}')

        if type(experiment_class) == ClusteringExperiment:
            experiment = experiment_class(method=algorithm, n_repeats=100)
        else:
            experiment = experiment_class(n_repeats=100)

        experiment.run()
        performance = experiment.performance_df.describe().assign(statistic=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
        performance.to_csv(os.path.join('data', f'performance_{algorithm}.csv'), index=False)

        median_mcc = performance.mcc.loc['50%']
        if median_mcc > best_performing_algorithm['median_mcc']:
            best_performing_algorithm['class'] = experiment_class
            best_performing_algorithm['algorithm'] = algorithm
            best_performing_algorithm['median_mcc'] = median_mcc

    print(f"Best-performing algorithm is {best_performing_algorithm['algorithm']} (MCC={best_performing_algorithm['median_mcc']})")
    print('Statistical analysis')

    if type(best_performing_algorithm['class']) == ClusteringExperiment:
        experiment = best_performing_algorithm['class'](method=best_performing_algorithm['algorithm'], n_repeats=1)
    else:
        experiment = best_performing_algorithm['class'](n_repeats=1)

    # Statistical analysis
    results = StatisticalAnalysis(estimator=experiment).run()
    results.to_csv(os.path.join('data', f'statistical_analysis_{best_performing_algorithm["algorithm"]}.csv'), index=False)

    print(f'\n[STATISTICAL ANALYSIS] Results of the statistical analysis:')
    print(results.to_markdown(index=False, tablefmt="grid"))
    print('Performance saved in folder data/')
else:
    exit(0)
