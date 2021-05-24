import pandas as pd
import requests
import yaml

from toscametrics.general.lines_code import LinesCode
from toscametrics.blueprint.num_interfaces import NumInterfaces
from toscametrics.blueprint.num_properties import NumProperties
from toscametrics.general.text_entropy import TextEntropy


def large_class_2_metrics():
    df = pd.read_csv('implementation/large_class.csv')

    for idx, row in df.iterrows():

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            pass

        # Decor defines Large class as a class with very high NMD + NAD, where NMD is the number of methods and NAD
        # is the number of attributes. In TOSCA we map the former to number of interfaces and the latter to the
        # number of properties
        try:
            # In the paper we define the Lazy Class smell as the inverse of the Large Class smell
            lines_code = int(LinesCode(plain_yml).count())
        except AttributeError:
            lines_code = 0

        try:
            num_interfaces = int(NumInterfaces(plain_yml).count())
        except AttributeError:
            num_interfaces = 0

        try:
            num_properties = int(NumProperties(plain_yml).count())
        except AttributeError:
            num_properties = 0

        try:
            entropy = TextEntropy(plain_yml).count()
        except AttributeError:
            entropy = 0

        df.loc[idx, 'lines_code'] = lines_code
        df.loc[idx, 'num_interfaces'] = num_interfaces
        df.loc[idx, 'num_properties'] = num_properties
        df.loc[idx, 'entropy'] = entropy

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
            df.loc[idx, 'lines_code'] = int(LinesCode(plain_yml).count())
        except AttributeError:
            df.loc[idx, 'lines_code'] = 0

        try:
            df.loc[idx, 'num_interfaces'] = int(NumInterfaces(plain_yml).count())
        except AttributeError:
            df.loc[idx, 'num_interfaces'] = 0
            continue

        try:
            df.loc[idx, 'num_properties'] = int(NumProperties(plain_yml).count())
        except AttributeError:
            df.loc[idx, 'num_properties'] = 0
            continue

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
