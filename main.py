import os
import pandas as pd

from experiments import exploratory_analysis, plot_performance, statistical_analysis

from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment
from experiments.threshold import StaticThresholdExperiment

print('Enter:\n- 1 for the exploratory analysis.\n- 2 to reproduce the empirical experiment.\n- 3 to reproduce the '
      'statistical analysis of performance.\n- 4 to plot algorithms\' performance.\n\nChoice:', end=' ')
value = input()

N_REPEATS = 100

# For test only
if value == '1':
    exploratory_analysis.main()

elif value == '3':
    statistical_analysis.main()

elif value == '4':
    plot_performance.main()

if value == '20':
    experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='spectral')  # ok (but warnings)
    experiment.run()
    print(experiment.performance_df.describe())
if value == '30':
    experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='affinity')
    experiment.run()
    print(experiment.performance_df.describe())
if value == '40':
    experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='agglomerative')
    experiment.run()
    print(experiment.performance_df.describe())
if value == '50':
    experiment = ClusteringExperiment(n_repeats=N_REPEATS, method='dbscan')
    experiment.run()
    print(experiment.performance_df.describe())

elif value == '9':
    experiment = StaticThresholdExperiment(n_repeats=N_REPEATS)
    experiment.run(multicollinearity_reduction=False)
    print(experiment.performance_df.describe())

# =====================================

elif value == '0':
    experiments = dict(
        iqr=IQRExperiment(n_repeats=N_REPEATS),
        mahalanobis=MahalanobisExperiment(n_repeats=N_REPEATS),
        # agglomerative=ClusteringExperiment(n_repeats=N_REPEATS, method='agglomerative'),
        birch=ClusteringExperiment(n_repeats=N_REPEATS, method='birch'),
        kmeans=ClusteringExperiment(n_repeats=N_REPEATS, method='kmeans'),
        mean_shift=ClusteringExperiment(n_repeats=N_REPEATS, method='mean-shift')
    )

    plot_data = pd.DataFrame(columns=['algorithm', 'measure', 'value'])

    for algorithm, experiment_obj in experiments.items():
        print(f'Running experiment using algorithm={algorithm}')

        experiment_obj.run()

        for _, row in experiment_obj.performance_df.iterrows():
            plot_data = plot_data.append([{
                'algorithm': algorithm,
                'measure': 'mcc',
                'value': row['mcc']
            }, {
                'algorithm': algorithm,
                'measure': 'f1',
                'value': row['f1']
            }], ignore_index=True)

        # Save performance
        experiment_obj.performance_df.to_csv(os.path.join('data', f'performance_{algorithm}.csv'), index=False)
        performance_local = experiment_obj.performance_df.describe().assign(
            statistic=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
        performance_local.to_csv(os.path.join('data', f'descriptive_performance_{algorithm}.csv'), index=False)

    exit()


else:
    exit(0)
