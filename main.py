import os
import pandas as pd
import scipy.stats as stats
from statistics import median

from copy import deepcopy

from experiments import exploratory_analysis, plot_performance, statistical_analysis
from experiments.experiment import AbstractExperiment
from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment
from experiments.threshold import StaticThresholdExperiment

print('Enter:\n- 1 for the exploratory analysis.\n- 2 to reproduce the empirical experiment.\n- 3 to reproduce the '
      'statistical analysis of performance.\n- 4 to plot algorithms\' performance.\n\nChoice:', end=' ')
value = input()

N_REPEATS = 100
FEATURES = 0
MCC = 1
PRECISION = 2
RECALL = 3

# For test only
if value == '1':
    exploratory_analysis.main()

elif value == '2':
    experiments = dict(
        iqr=IQRExperiment(),
        mahalanobis=MahalanobisExperiment(),
        agglomerative=ClusteringExperiment(method='agglomerative'),
        birch=ClusteringExperiment(method='birch'),
        kmeans=ClusteringExperiment(method='kmeans'),
        mean_shift=ClusteringExperiment(method='mean-shift'),
        spectral=ClusteringExperiment(method='spectral')
    )

    for algorithm, current_experiment in experiments.items():
        print(f'Running experiment using algorithm={algorithm}')

        used_features = []

        if algorithm == 'mahalanobis':
            used_features.append('lcot')

        yet_to_use_features = {'lines_code', 'lcot', 'num_types_and_templates', 'num_interfaces', 'num_properties', 'num_imports'} - set(used_features)
        sfs_df = pd.DataFrame()  # Stepwise forward selection dataframe
        optimal_experiment = None

        while len(yet_to_use_features) > 0:
            step_best_experiment = AbstractExperiment()

            for feature in yet_to_use_features:
                # print('Using', [*used_features, feature])
                current_experiment.run(features=[*used_features, feature], n_repeats=N_REPEATS)

                if current_experiment.median_mcc > step_best_experiment.median_mcc:
                    step_best_experiment = deepcopy(current_experiment)

            # MCC is used to select the optimal attribute at each step.
            # Once the optimal attribute subset is obtained, the stats for that are retained
            if not optimal_experiment:
                optimal_experiment = step_best_experiment
            else:
                _, p_value = stats.mannwhitneyu(step_best_experiment.performance_df.mcc,
                                                optimal_experiment.performance_df.mcc,
                                                alternative='greater')

                if step_best_experiment.median_mcc > optimal_experiment.median_mcc and p_value < 0.05:
                    optimal_experiment = step_best_experiment

            used_features = step_best_experiment.features
            yet_to_use_features -= set(used_features)

            sfs_df = sfs_df.append({
                'features': used_features,
                'median_mcc': step_best_experiment.median_mcc,
                'median_precision': step_best_experiment.median_precision,
                'median_recall': step_best_experiment.median_recall,
            }, ignore_index=True)

        sfs_df.to_csv(os.path.join('data', 'feature-selection', f'{algorithm}.csv'), index=True)

        print(sfs_df.to_markdown(index=False, tablefmt="grid"))
        print('Optimal subset:', optimal_experiment.features,
              'Median MCC:', optimal_experiment.median_mcc,
              'Median Precision:', optimal_experiment.median_precision,
              'Median Recall:', optimal_experiment.median_recall)
        print(optimal_experiment.performance_df.describe())

        # Save performance
        optimal_experiment.performance_df.to_csv(os.path.join('data', 'performance', f'{algorithm}.csv'), index=False)
        performance_local = optimal_experiment.performance_df.describe().assign(
            statistic=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
        performance_local.to_csv(os.path.join('data', 'performance', f'{algorithm}_descriptive.csv'), index=False)

elif value == '3':
    statistical_analysis.main()

elif value == '4':
    plot_performance.main()

#
# if value == '30':
#     experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='affinity')
#     experiment.run()
#     print(experiment.performance_df.describe())
#
# if value == '50':
#     experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='dbscan')
#     experiment.run()
#     print(experiment.performance_df.describe())
#
# elif value == '9':
#     experiment = StaticThresholdExperiment(n_repeats=N_REPEATS)
#     experiment.run(multicollinearity_reduction=False)
#     print(experiment.performance_df.describe())

else:
    exit(0)
