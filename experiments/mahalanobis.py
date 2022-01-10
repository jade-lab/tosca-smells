import numpy as np

from .experiment import AbstractExperiment
from scipy.stats import chi2


class MahalanobisExperiment(AbstractExperiment):

    def __init__(self):
        super(self.__class__, self).__init__()

    def detect_smells(self, dataset):

        def mahalanobis(x=None, data=None, cov=None):
            x_mu = x - np.mean(data)
            if not cov:
                cov = np.cov(data.values.T)
            inv_covmat = np.linalg.inv(cov)
            left = np.dot(x_mu, inv_covmat)
            mahal = np.dot(left, x_mu.T)
            return mahal.diagonal()

        dataset_loc = dataset.copy()

        # calculate Mahalanobis distances for each row
        distances = mahalanobis(x=dataset, data=dataset[dataset.columns])
        degrees_of_freedom = dataset.shape[1] # - 1

        # calculate p-value for each mahalanobis distance
        dataset_loc['p'] = 1 - chi2.cdf(distances, degrees_of_freedom)

        for idx, row in dataset_loc.iterrows():
            yield idx, row['p'] < 0.001
