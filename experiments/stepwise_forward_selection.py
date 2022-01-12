import json
import matplotlib.pyplot as plt
import os
import pandas as pd


def main():

    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)

    for algorithm in ('iqr', 'mean_shift', 'mahalanobis', 'kmeans', 'birch', 'agglomerative'):

        data = pd.read_csv(os.path.join('data', 'feature-selection', f'{algorithm}.csv'))

        x = [json.loads(features.replace("\'", "\""))[-1] for features in data.features]
        y_mcc = data.median_mcc.to_list()
        y_precision = data.median_precision.to_list()
        y_recall = data.median_recall.to_list()

        plt.plot(x, y_mcc, label="mcc", linestyle='-', marker='.',  linewidth=2)
        plt.plot(x, y_precision, label="precision", linestyle='-', marker='.',  linewidth=2)
        plt.plot(x, y_recall, label="recall", linestyle=':', marker='.',  linewidth=2)

        plt.title(algorithm.upper())
        plt.legend()
        plt.show()
