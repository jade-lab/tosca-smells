import numpy as np
import pandas as pd


def large_class_threshold(df: pd.DataFrame):
    """Return the threshold Tup over which the code is considered LARGE CLASS"""
    metrics_sum = df.sum(axis=1)
    q3 = np.quantile(metrics_sum, 0.75)
    q1 = np.quantile(metrics_sum, 0.25)
    iqr = q3 - q1
    return q3 + 1.5*iqr


def lazy_class_threshold(df: pd.DataFrame):
    """Return the threshold Tup over which the code is considered LAZY CLASS"""
    metrics_sum = df.sum(axis=1)
    metrics_sum = metrics_sum.loc[metrics_sum != 0]

    print(metrics_sum)

    q3 = np.quantile(metrics_sum, 0.75)
    q1 = np.quantile(metrics_sum, 0.25)
    iqr = q3 - q1

    return q1 - 1.5*iqr


def long_method_threshold(df: pd.DataFrame):
    """Return the threshold Tup over which the code is considered LONG METHOD"""
    q3 = np.quantile(df.lines_code, 0.75)
    q1 = np.quantile(df.lines_code, 0.25)
    iqr = q3 - q1

    return q3 + 1.5*iqr


# Test
# large_class_df = pd.read_csv('implementation/large_class.csv').drop(['id', 'type', 'smelly'], axis=1).fillna(0)
# print(large_class_threshold(large_class_df))
# print(large_class_df[large_class_df.num_interfaces + large_class_df.num_properties > 7.5].shape)
#
from sklearn.preprocessing import MinMaxScaler
lazy_class_df = pd.read_csv('implementation/large_class.csv').drop(['id', 'type', 'smelly'], axis=1).fillna(0)
lazy_class_df = pd.DataFrame(MinMaxScaler().fit_transform(lazy_class_df))
print(lazy_class_threshold(lazy_class_df))
#
# long_method_df = pd.read_csv('implementation/long_method.csv').drop(['id', 'url', 'smelly'], axis=1).fillna(0)
# print(long_method_threshold(long_method_df))


