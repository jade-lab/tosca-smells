import numpy as np

from .experiment import AbstractExperiment


class IQRExperiment(AbstractExperiment):

    def __init__(self, n_repeats: int = 100):
        super(self.__class__, self).__init__(n_repeats)

    def detect_smells(self, dataset):

        thresholds = dict()

        # calculate threshold for every metrics
        for metric in dataset.columns:
            q1, q3 = np.percentile(dataset[metric], [25, 75])
            iqr = q3 - q1
            thresholds[metric] = round(q3 + (1.5 * iqr), 2)

        for idx, row in dataset.iterrows():

            for metric, threshold in thresholds.items():
                is_smelly = False

                if row[metric] > threshold:
                    is_smelly = True
                    break

            yield idx, is_smelly
