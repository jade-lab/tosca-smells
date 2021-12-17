import os
import pandas as pd
import scipy.stats as stats
from cliffs_delta import cliffs_delta


def main():

    # Load data
    plot_data = pd.DataFrame()

    for algorithm in ('agglomerative', 'birch', 'iqr', 'kmeans', 'mahalanobis', 'mean_shift'):

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

    print('Results saved in data/STATISTICAL_ANALYSIS.md')
