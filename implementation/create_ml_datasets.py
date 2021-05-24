import os
import pandas as pd
import requests
import yaml

from toscametrics.general.lines_code import LinesCode
from toscametrics.general.num_tokens import NumTokens
from toscametrics.general.text_entropy import TextEntropy
from toscametrics.blueprint.num_interfaces import NumInterfaces
from toscametrics.blueprint.num_properties import NumProperties


def large_class_2_metrics():
    df = pd.read_csv(os.path.join('implementation', 'datasets', 'large_class.csv'))

    for idx, row in df.iterrows():
        plain_yml = ''

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
        except (AttributeError, TypeError):
            lines_code = 0

        try:
            num_interfaces = int(NumInterfaces(plain_yml).count())
        except (AttributeError, TypeError):
            num_interfaces = 0

        try:
            num_properties = int(NumProperties(plain_yml).count())
        except (AttributeError, TypeError):
            num_properties = 0

        try:
            num_tokens = NumTokens(plain_yml).count()
        except (AttributeError, TypeError):
            num_tokens = 0

        try:
            entropy = TextEntropy(plain_yml).count()
        except (AttributeError, TypeError):
            entropy = 0

        df.loc[idx, 'lines_code'] = lines_code
        df.loc[idx, 'num_interfaces'] = num_interfaces
        df.loc[idx, 'num_properties'] = num_properties
        df.loc[idx, 'num_tokens'] = num_tokens
        df.loc[idx, 'entropy'] = entropy

    return df.drop(['type'], axis=1)


def lazy_class_2_metrics():
    df = pd.read_csv(os.path.join('implementation', 'datasets', 'lazy_class.csv'))

    for idx, row in df.iterrows():

        plain_yml = ''

        try:
            plain_yml = yaml.safe_dump(yaml.safe_load(row.type))
        except yaml.YAMLError:
            pass

        # In the paper we define the Lazy Class smell as the inverse of the Large Class smell
        try:
            lines_code = int(LinesCode(plain_yml).count())
        except (AttributeError, TypeError):
            lines_code = 0

        try:
            num_interfaces = int(NumInterfaces(plain_yml).count())
        except (AttributeError, TypeError):
            num_interfaces = 0

        try:
            num_tokens = NumTokens(plain_yml).count()
        except (AttributeError, TypeError):
            num_tokens = 0

        try:
            num_properties = int(NumProperties(plain_yml).count())
        except (AttributeError, TypeError):
            num_properties = 0

        try:
            entropy = TextEntropy(plain_yml).count()
        except (AttributeError, TypeError):
            entropy = 0

        df.loc[idx, 'lines_code'] = lines_code
        df.loc[idx, 'num_interfaces'] = num_interfaces
        df.loc[idx, 'num_properties'] = num_properties
        df.loc[idx, 'num_tokens'] = num_tokens
        df.loc[idx, 'entropy'] = entropy

    return df.drop(['type'], axis=1)


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
