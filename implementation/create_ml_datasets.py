import pandas as pd
import requests
import yaml

from toscametrics.general.lines_code import LinesCode
from toscametrics.blueprint.num_interfaces import NumInterfaces
from toscametrics.blueprint.num_properties import NumProperties


def large_class_2_metrics():
    df = pd.read_csv('implementation/large_class.csv')

    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            continue

        try:
            # Decor defines Large class as a class with very high NMD + NAD, where NMD is the number of methods and NAD
            # is the number of attributes. In TOSCA we map the former to number of interfaces and the latter to the
            # number of properties
            df.loc[idx, 'num_interfaces'] = NumInterfaces(plain_yml).count()
            df.loc[idx, 'num_properties'] = NumProperties(plain_yml).count()

        except AttributeError:
            continue

    # Remove columns containing only zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    df.to_csv('implementation/large_class_metrics.csv', index=False)


def lazy_class_2_metrics():
    df = pd.read_csv('implementation/lazy_class.csv')

    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            continue

        try:
            # In the paper we define the Lazy Class smell as the inverse of the Large Class smell
            df.loc[idx, 'num_interfaces'] = NumInterfaces(plain_yml).count()
            df.loc[idx, 'num_properties'] = NumProperties(plain_yml).count()
        except AttributeError:
            continue

    # Remove columns containing only zeros
    df = df.loc[:, (df != 0).any(axis=0)]
    df.to_csv('implementation/lazy_class_metrics.csv', index=False)


def long_method_2_metrics():
    df = pd.read_csv('implementation/long_method.csv')

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
    df.to_csv('implementation/long_method_metrics.csv', index=False)


print('Creating dataset: large_class_metrics.csv')
large_class_2_metrics()

print('Creating dataset: lazy_class_metrics.csv')
lazy_class_2_metrics()

print('Creating dataset: long_method_metrics.csv')
long_method_2_metrics()
