import pandas as pd
import requests
import yaml

from toscametrics.metrics_extractor import extract_all
from toscametrics.general.lines_code import LinesCode


def large_class_2_metrics():
    df = pd.read_csv('validation/large_class.csv')

    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            continue

        try:
            metrics = extract_all(plain_yml)
        except AttributeError:
            continue

        for key, value in metrics.items():
            df.loc[idx, key] = value

    # Remove columns containing only zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    df.to_csv('./implementation/large_class.csv', index=False)


def lazy_class_2_metrics():
    df = pd.read_csv('validation/lazy_class.csv')

    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            continue

        try:
            metrics = extract_all(plain_yml)
        except AttributeError:
            continue

        for key, value in metrics.items():
            df.loc[idx, key] = value

    # Remove columns containing only zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    df.to_csv('./implementation/lazy_class.csv', index=False)


def long_method_2_metrics():
    df = pd.read_csv('validation/long_method.csv')

    for idx, row in df.iterrows():
        response = requests.get(row.url)
        if response.status_code != 200:
            continue

        try:
            df.loc[idx, 'lines_code'] = LinesCode(response.text).count()
        except TypeError:
            continue

    # Remove columns containing only zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    df.to_csv('./implementation/long_method.csv', index=False)


print('Creating dataset: large_class.csv')
large_class_2_metrics()

print('Creating dataset: lazy_class.csv')
lazy_class_2_metrics()

print('Creating dataset: long_method.csv')
long_method_2_metrics()
