import os
import pandas as pd
import requests
import yaml

from toscametrics.metrics_extractor import extract_all
from toscametrics.general.lines_code import LinesCode
from toscametrics.general.num_keys import NumKeys
from toscametrics.general.num_tokens import NumTokens
from toscametrics.general.text_entropy import TextEntropy
from toscametrics.blueprint.num_interfaces import NumInterfaces
from toscametrics.blueprint.num_imports import NumImports
from toscametrics.blueprint.num_inputs import NumInputs
from toscametrics.blueprint.num_parameters import NumParameters
from toscametrics.blueprint.num_properties import NumProperties


def extract_all_metrics(df: pd.DataFrame):
    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
            for name, metric in extract_all(plain_yml).items():
                try:
                    # In the paper we define the Lazy Class smell as the inverse of the Large Class smell
                    df.loc[idx, name] = metric
                except (AttributeError, TypeError):
                    df.loc[idx, name] = 0

        except yaml.YAMLError:
            continue

    return df.drop(['type'], axis=1)


def large_class_2_metrics():
    df = pd.read_csv(os.path.join('implementation', 'datasets', 'large_class.csv'))
    return extract_all_metrics(df)


def lazy_class_2_metrics():
    df = pd.read_csv(os.path.join('implementation', 'datasets', 'lazy_class.csv'))
    return extract_all_metrics(df)


def long_method_2_metrics():
    df = pd.read_csv(os.path.join('implementation', 'datasets', 'long_method.csv'))

    for idx, row in df.iterrows():
        response = requests.get(row.url)
        if response.status_code != 200:
            continue

        try:
            df.loc[idx, 'lines_code'] = LinesCode(response.text).count()
        except TypeError:
            continue

    return df.drop(['url'], axis=1)
