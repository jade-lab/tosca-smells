import os
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from cliffs_delta import cliffs_delta


def main():
    plt.rc('ytick', labelsize=12)
    plt.rc('xtick', labelsize=12)
    plt.rc('axes', labelsize=14)

    metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)
    metrics_df['num_types_and_templates'] = metrics_df[['num_node_templates', 'num_relationship_templates',
                                                        'num_node_types', 'num_relationship_types']].sum(axis=1)
    metrics_df = metrics_df[['url', 'lines_code', 'lcot', 'num_types_and_templates', 'num_interfaces', 'num_properties',
                             'num_imports']]

    validation_df = pd.read_csv(os.path.join('data', 'validation.csv'))
    group_all = metrics_df.merge(validation_df[['url', 'final']], on='url')
    group_smelly = group_all[group_all.final == True].drop(['url', 'final'], axis=1)
    group_sound = group_all[group_all.final == False].drop(['url', 'final'], axis=1)

    results = pd.DataFrame()
    n_tests = group_smelly.columns.size

    for feature in group_smelly.columns:

        u_stat, p_value = stats.mannwhitneyu(group_smelly[feature], group_sound[feature], alternative='greater')
        d, res = cliffs_delta(group_smelly[feature], group_sound[feature])

        results = results.append({
            'feature': feature.upper(),
            'p-value': p_value,
            'p-value corrected': p_value * n_tests,
            'U': u_stat,
            'cliff_delta': d,
            'mean smelly': round(group_smelly[feature].mean()),
            'mean sound': round(group_sound[feature].mean()),
            'significant': '**yes**' if p_value * n_tests < 0.01 else 'no'
        }, ignore_index=True)

    ncols = 3
    nrows = round((group_all.shape[1] - 2) / 3)
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)

    i = 0
    j = 0

    for metric in group_all.columns:
        if metric in ('smelly', 'url', 'final'):
            continue

        # Combine data
        plot_data = list([group_smelly[metric], group_sound[metric]])

        xticklabels = ['Blob', 'Sound']

        axs[i, j % ncols].set_xlabel(metric.replace('_', ' ').upper())
        axs[i, j % ncols].set_xticks([1, 2])
        axs[i, j % ncols].set_xticklabels(xticklabels)
        parts = axs[i, j % ncols].violinplot(plot_data, showmedians=True, quantiles=[(0.25, 0.75), (0.25, 0.75)])

        for pc in parts['bodies']:
            pc.set_facecolor('#b3efff')
            pc.set_alpha(1)

        j += 1

        if j % ncols == 0:
            i += 1

    plt.show()

    print('\nFor each metric, the table below reports results of the statistical analysis of the metric distribution '
          'within Blob blueprints against all other blueprints:')

    with open(os.path.join('data', 'EXPLORATORY_ANALYSIS.md'), 'w') as f:
        results.to_markdown(buf=f, index=False)

    print(results.to_markdown(index=False, tablefmt="grid"))
    print('Results saved in data/EXPLORATORY_ANALYSIS.md')