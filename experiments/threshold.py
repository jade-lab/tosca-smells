from .experiment import AbstractExperiment


class StaticThresholdExperiment(AbstractExperiment):

    def __init__(self, n_repeats: int = 100, threshold: int = 7):
        super(self.__class__, self).__init__(n_repeats)
        self.threshold = threshold

    def detect_smells(self, dataset):
        for idx, row in dataset.iterrows():
            is_smelly = row['num_types_and_templates'] > 1 or row['lines_code'] > 40 or row['lcot'] > 1
            yield idx, is_smelly
