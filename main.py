import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

from cliffs_delta import cliffs_delta
from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment
from experiments.exploratory_analysis import ExploratoryAnalysis
from experiments.threshold import StaticThresholdExperiment

print('Enter:\n- 1 for the exploratory analysis.\n- 2 to reproduce the empirical experiment.\n- 3 to reproduce the '
      'statistical analysis of performance.\n- 4 to plot algorithms\' performance.\n\nChoice:', end=' ')
value = input()

N_REPEATS = 100

# For test only
if value == '1':
    # Statistical analysis on the ground truth
    results = ExploratoryAnalysis().run()
    results.to_csv(os.path.join('data', f'statistical_analysis_metrics.csv'), index=False)
    print('\nFor each metric, the table below reports results of the statistical analysis of the metric distribution '
          'within Blob blueprints against all other blueprints:')
    print(results.to_markdown(index=False, tablefmt="grid"))
    print('Results saved in data/statistical_analysis.csv')

elif value == '3':

    # Load data
    plot_data = pd.DataFrame()

    for algorithm in ('birch', 'iqr', 'kmeans', 'mahalanobis', 'mean_shift'):

        for _, row in pd.read_csv(os.path.join('data', f'performance_{algorithm}.csv')).iterrows():
            plot_data = plot_data.append([{
                'algorithm': algorithm,
                'measure': 'mcc',
                'value': row['mcc']
            }, {
                'algorithm': algorithm,
                'measure': 'f1',
                'value': row['f1']
            }, {
                'algorithm': algorithm,
                'measure': 'precision',
                'value': row['precision']
            }, {
                'algorithm': algorithm,
                'measure': 'recall',
                'value': row['recall']
            }, {
                'algorithm': algorithm,
                'measure': 'ari',
                'value': row['ari']
            }], ignore_index=True)

    # Perform statistical analysis
    n_tests = len(plot_data.algorithm.unique())

    content = '# Statistical Evaluation of Techniques'

    for measure in ('mcc', 'f1', 'precision', 'recall', 'ari'):
        statistical_analysis_df = pd.DataFrame()

        for algorithm1 in plot_data.algorithm.unique():

            for algorithm2 in plot_data.algorithm.unique():

                if algorithm1 == algorithm2:
                    continue

                if measure == 'ari' and (
                        algorithm1 in ('iqr', 'mahalanobis') or algorithm2 in ('iqr', 'mahalanobis')):
                    continue

                mask_algo1 = (plot_data.algorithm == algorithm1) & (plot_data.measure == measure)
                mask_algo2 = (plot_data.algorithm == algorithm2) & (plot_data.measure == measure)

                u_stat, p_value = stats.mannwhitneyu(plot_data[mask_algo1].value, plot_data[mask_algo2].value,
                                                     alternative='greater')
                d, res = cliffs_delta(plot_data[mask_algo1].value, plot_data[mask_algo2].value)

                statistical_analysis_df = statistical_analysis_df.append({
                    'algorithm 1': algorithm1,
                    'algorithm 2': algorithm2,
                    'p-value': p_value,
                    'p-value corrected': p_value * n_tests,
                    'U': u_stat,
                    'cliff_delta': d,
                    'mean algorithm 1': round(plot_data[mask_algo1].value.mean(), 4),
                    'mean algorithm 2': round(plot_data[mask_algo2].value.mean(), 4),
                    'measure': measure,
                    'significant': '**yes**' if p_value * n_tests < 0.01 else 'no'
                }, ignore_index=True)

        content += f'\n## {measure.upper()}\n'
        content += statistical_analysis_df.to_markdown(index=False)
        print(statistical_analysis_df.to_markdown(index=False, tablefmt="grid"))

    with open(os.path.join('data', f'STATISTICAL_ANALYSIS.md'), 'w') as f:
        f.write(content)

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
    # Violin plot to compare techniques (MCC)
    iqr_mcc_mask = (plot_data.algorithm == 'iqr') & (plot_data.measure == 'mcc')
    mahalanobis_mcc_mask = (plot_data.algorithm == 'mahalanobis') & (plot_data.measure == 'mcc')
    birch_mcc_mask = (plot_data.algorithm == 'birch') & (plot_data.measure == 'mcc')
    kmeans_mcc_mask = (plot_data.algorithm == 'kmeans') & (plot_data.measure == 'mcc')
    mean_shift_mcc_mask = (plot_data.algorithm == 'mean_shift') & (plot_data.measure == 'mcc')

    fig, ax = plt.subplots()
    ax.violinplot([plot_data[iqr_mcc_mask].value,
                   plot_data[mahalanobis_mcc_mask].value,
                   plot_data[birch_mcc_mask].value,
                   plot_data[kmeans_mcc_mask].value,
                   plot_data[mean_shift_mcc_mask].value], showmedians=True, showextrema=True)

    xticklabels = ['IQR', 'Mahalanobis', 'Birch', 'KMeans', 'MeanShift']
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(xticklabels)
    plt.show()


else:
    exit(0)
