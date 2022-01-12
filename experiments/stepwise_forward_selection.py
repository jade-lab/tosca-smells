import json
import matplotlib.pyplot as plt
import os
import pandas as pd


def main():

    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)

    figure, axis = plt.subplots(3, 2)

    i = 0
    j = 0
    for algorithm in ('iqr', 'mean_shift', 'mahalanobis', 'kmeans', 'birch', 'agglomerative'):

        data = pd.read_csv(os.path.join('data', 'feature-selection', f'{algorithm}.csv'))

        x = []
        for features in data.features:
            feature = json.loads(features.replace("\'", "\""))[-1]
            if feature == 'num_types_and_templates':
                feature = 'num_types'
            x.append(feature)

        y_mcc = data.median_mcc.to_list()
        y_precision = data.median_precision.to_list()
        y_recall = data.median_recall.to_list()

        axis[i, j % 2].plot(x, y_mcc, label="mcc", linestyle='-', marker='.',  linewidth=2)
        axis[i, j % 2].plot(x, y_precision, label="precision", linestyle='-', marker='.',  linewidth=2)
        axis[i, j % 2].plot(x, y_recall, label="recall", linestyle=':', marker='.',  linewidth=2)
        axis[i, j % 2].set_title(algorithm)

        j += 1

        if j % 2 == 0:
            i += 1

    plt.legend()
    plt.show()
