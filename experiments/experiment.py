import os
import pandas as pd
import progressbar
import random

from .utilities import calculate_performance, normalize, reduce_multicollinearity


class AbstractExperiment:

    def __init__(self):
        self.performance_df = pd.DataFrame()
        self.features = []
        self.evaluation_sets = None
        random.seed(42)

    @staticmethod
    def load_dataset():
        # Load metrics dataset
        df = pd.read_csv(os.path.join('data', 'metrics.csv')).fillna(0)

        # Remove duplicates based on metrics value
        df.drop_duplicates(subset=df.columns.difference(['url']), keep='first', inplace=True)

        # TODO: move this in metrics extraction
        df['num_types_and_templates'] = df[['num_node_templates', 'num_relationship_templates',
                                            'num_node_types', 'num_relationship_types']].sum(axis=1)

        return df

    def run(self, features: list = None, n_repeats: int = 100):
        """

        Parameters
        ----------
        features: list
            the list of features to use

        n_repeats: int
            number of times to repeat the experiment on n_repeats perturbed versions of the original dataset. \
            If n_repeats = 1 the original dataset is used

        Returns
        -------
        None

        """
        metrics_df = self.load_dataset()

        if features:
            self.features = features
            metrics_df = metrics_df.loc[:, [*features, 'url']]

        # Create n_repeats evaluation datasets to run the algorithms on
        self.evaluation_sets = []

        if n_repeats == 1:
            # Use the original dataset
            self.evaluation_sets.append(metrics_df)
        else:
            # Create n_repeats perturbed versions of the original dataset of at least 290 uniformly sampled observations
            # without replacement (290 is a statistically relevant sample based on the original dataset's size)
            for i in range(0, n_repeats):
                self.evaluation_sets.append(
                    metrics_df.sample(n=random.randint(290, metrics_df.shape[0]), random_state=42))

        # Initialize performance dataframe
        self.performance_df = pd.DataFrame()

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

            self.performance_df = self.performance_df.append(performance, ignore_index=True)

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

    @property
    def median_mcc(self):
        return self.performance_df.mcc.median() if 'mcc' in self.performance_df else -1

    @property
    def median_precision(self):
        return self.performance_df.precision.median() if 'precision' in self.performance_df else 0

    @property
    def median_recall(self):
        return self.performance_df.recall.median() if 'recall' in self.performance_df else -1
