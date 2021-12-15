import os
import numpy as np
import pandas as pd
import progressbar
import random

from .utilities import calculate_performance, normalize, reduce_multicollinearity


class AbstractExperiment:

    def __init__(self, n_repeats: int = 100):
        random.seed(42)

        # Store the values of ARI, MCC, Precision, and Recall across the experiment iterations
        self.performance_df = pd.DataFrame()

        # Load metrics dataset
        metrics_df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

        # Remove duplicates based on metrics value
        metrics_df.drop_duplicates(subset=metrics_df.columns.difference(['url']), keep='first', inplace=True)

        # Node templates + Relationship templates = num_templates (as define in puppet (abstraction))
        metrics_df['num_types_and_templates'] = metrics_df[['num_node_templates', 'num_relationship_templates',
                                                            'num_node_types', 'num_relationship_types']].sum(axis=1)
        metrics_df['complexity'] = metrics_df[['lcot', 'num_interfaces', 'num_properties']].sum(axis=1)

        metrics_df = metrics_df[['url', 'lines_code', 'num_types_and_templates', 'complexity']]

        # Create n_repeats evaluation datasets to run the algorithms on
        self.evaluation_sets = []

        if n_repeats == 1:
            # Use the entire original dataset
            self.evaluation_sets.append(metrics_df)
        else:
            for i in range(0, n_repeats):
                self.evaluation_sets.append(metrics_df.sample(n=random.randint(290, metrics_df.shape[0]), random_state=42))

    def run(self, multicollinearity_reduction: bool = True):
        """

        Parameters
        ----------
        multicollinearity_reduction : bool
            if to reduce multicollinearity among predictors (where VIF > 10)

        Returns
        -------
        None

        """
        for i in progressbar.progressbar(range(len(self.evaluation_sets))):

            # Prepare data
            X = self.evaluation_sets[i].drop(['url'], axis=1)

            # Remove correlated variables (i.e., features for which VIF > 10)
            if multicollinearity_reduction:
                reduce_multicollinearity(X, print_result=False)

            # Normalize dataset
            _, X = normalize(X)

            for idx, is_smelly in self.detect_smells(X):
                X.loc[idx, 'smelly'] = is_smelly

            performance = calculate_performance(self.evaluation_sets[i].assign(smelly=X.smelly.to_list()),
                                                print_result=False)

            self.performance_df = self.performance_df.append({
                'ari': performance['ari'],
                'mcc': performance['mcc'],
                'precision': performance['precision'],
                'recall': performance['recall'],
            }, ignore_index=True)

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
