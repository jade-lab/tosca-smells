import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

def main():
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

    # Violin plot for each evaluation measure
    for measure in ('mcc', 'f1'):

        # Violin plot to compare techniques (MCC)
        iqr_mask = (plot_data.algorithm == 'iqr') & (plot_data.measure == measure)
        mahalanobis_mask = (plot_data.algorithm == 'mahalanobis') & (plot_data.measure == measure)
        birch_mask = (plot_data.algorithm == 'birch') & (plot_data.measure == measure)
        kmeans_mask = (plot_data.algorithm == 'kmeans') & (plot_data.measure == measure)
        mean_shift_mask = (plot_data.algorithm == 'mean_shift') & (plot_data.measure == measure)

        fig, ax = plt.subplots()
        fig.suptitle(f'{measure.upper()} across techniques')
        ax.violinplot([plot_data[iqr_mask].value,
                       plot_data[mahalanobis_mask].value,
                       plot_data[birch_mask].value,
                       plot_data[kmeans_mask].value,
                       plot_data[mean_shift_mask].value],
                      showmedians=True,
                      showextrema=True,
                      quantiles=[(0.25, 0.75), (0.25, 0.75), (0.25, 0.75), (0.25, 0.75), (0.25, 0.75)])

        ax.set_xticks([1, 2, 3, 4, 5])
        ax.set_xticklabels(['IQR', 'Mahalanobis', 'Birch', 'KMeans', 'MeanShift'])
        plt.ylabel = measure.upper()
        plt.show()
