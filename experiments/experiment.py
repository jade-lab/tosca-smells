import os
import numpy as np
import pandas as pd
import progressbar
import random

from .utilities import calculate_performance, normalize, reduce_multicollinearity


class AbstractExperiment:

    def __init__(self, n_repeats: int = 100):
        random.seed(42)

        # Store the values of MCC, precision, and recall across the experiment iterations
        self.mcc = []
        self.precision = []
        self.recall = []

        # Load dataset
        metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

        # Create n_repeats evaluation datasets to run the algorithms on
        self.evaluation_sets = []

        for i in range(0, n_repeats):
            self.evaluation_sets.append(metrics_df.sample(n=random.randint(100, metrics_df.shape[0]), random_state=42))

    def run(self):
        for i in progressbar.progressbar(range(len(self.evaluation_sets))):

            # Prepare data
            X = self.evaluation_sets[i].drop(['url'], axis=1)

            # Remove correlated variables (i.e., features for which VIF > 10)
            reduce_multicollinearity(X, print_result=False)

            # Normalize dataset
            _, X = normalize(X)

            for idx, is_smelly in self.detect_smells(X):
                X.loc[idx, 'smelly'] = is_smelly

            performance = calculate_performance(self.evaluation_sets[i].assign(smelly=X.smelly.to_list()),
                                                print_result=False)
            self.mcc.append(performance['mcc'])
            self.precision.append(performance['precision'])
            self.recall.append(performance['recall'])

    def detect_smells(self, dataset: pd.DataFrame):
        """ For every observation in the dataset, compute the detection strategy and return a generator consisting of
        a tuple (int, bool) where the first item is the index of that observation and the second items is a boolean
        indicating if that observation is detected as smell

        Parameters
        ----------
        dataset : pd.DataFrame
            A pre-processed pandas dataframe

        Yields
        ------
        tuple : ndarray
            The tuple (int, bool) of index and smelliness for that observation
        """
        yield NotImplementedError

    def print_performance(self):
        print(f'Median MCC: {np.median(self.mcc)}\n' +
              f'Median precision: {np.median(self.precision)}\n' +
              f'Median recall: {np.median(self.recall)}')
