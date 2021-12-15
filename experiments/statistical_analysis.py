import pandas as pd
import scipy.stats as stats

from cliffs_delta import cliffs_delta
from experiments.clustering import ClusteringExperiment
from experiments.iqr import IQRExperiment
from experiments.mahalanobis import MahalanobisExperiment

from .experiment import AbstractExperiment
from .utilities import normalize, reduce_multicollinearity, statistical_analysis


class StatisticalAnalysis:

    def __init__(self, estimator: AbstractExperiment):
        """

        Parameters
        ----------
        estimator: AbstractExperiment
            An Experiment class. Options: IQRExperiment, MahalanobisExperiment, KMeansExperiment, ...
        """

        if type(estimator) not in (IQRExperiment, MahalanobisExperiment, ClusteringExperiment):
            raise ValueError()

        self.estimator = estimator

    def run(self, multicollinearity_reduction: bool = True):
        # Prepare data
        X = self.estimator.evaluation_sets[0].drop(['url'], axis=1)

        # Remove correlated variables (i.e., features for which VIF > 10)
        if multicollinearity_reduction:
            reduce_multicollinearity(X, print_result=False)

        # Normalize dataset
        _, X = normalize(X)

        for idx, is_smelly in self.estimator.detect_smells(X):
            X.loc[idx, 'smelly'] = is_smelly

        group_all = self.estimator.evaluation_sets[0].assign(smelly=X.smelly.to_list())
        group_smelly = group_all[group_all.smelly == True]
        group_sound = group_all[group_all.smelly == False]

        results = pd.DataFrame()
        n_tests = group_smelly.columns.size

        for feature in group_smelly.columns:

            if feature == 'smelly':
                continue

            u_stat, p_value = stats.mannwhitneyu(group_smelly[feature], group_sound[feature], alternative='greater')
            d, res = cliffs_delta(group_sound[feature], group_sound[feature])

            if p_value * n_tests < 0.01:
                results = results.append({
                    'feature': feature.upper(),
                    'p-value': p_value,
                    'p-value corrected': p_value * n_tests,
                    'U': u_stat,
                    'cliff_delta': d,
                    'mean smelly': round(group_smelly[feature].mean()),
                    'mean sound': round(group_sound[feature].mean()),
                    # 'count smelly': len(cluster_smelly[feature]),
                    # 'count sound': len(cluster_sound[feature])
                }, ignore_index=True)

        return results
