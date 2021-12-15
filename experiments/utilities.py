import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from cliffs_delta import cliffs_delta
from sklearn.metrics import confusion_matrix, matthews_corrcoef, precision_score, recall_score, adjusted_rand_score
from sklearn.preprocessing import RobustScaler

from statsmodels.stats.outliers_influence import variance_inflation_factor


def reduce_multicollinearity(df: pd.DataFrame, threshold: int = 10, print_result: bool = True):
    vif_results = pd.DataFrame()

    while True:
        vif_data = pd.DataFrame()
        vif_data["feature"] = df.columns
        vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]

        if any([vif > threshold for vif in vif_data.VIF]):
            # Remove feature with the highest VIF
            idx = vif_data[['VIF']].idxmax().iloc[0]
            df.drop(vif_data.iloc[idx].feature, axis=1, inplace=True)

            vif_results = vif_results.append({
                'feature': vif_data.iloc[idx].feature.upper(),
                'VIF': vif_data.iloc[idx].VIF
            }, ignore_index=True)

        else:
            break

    if print_result:
        print(f'\n[MULTICOLLINEARITY REDUCTION] Metrics removed from the dataset as result of multicollinearity '
              f'reduction (VIF > {threshold}):')
        print(vif_results.to_markdown(index=False, tablefmt="grid"))


def normalize(df: pd.DataFrame):
    columns = df.columns
    normalizer = RobustScaler()
    return normalizer, pd.DataFrame(normalizer.fit_transform(df), columns=columns)


def calculate_performance(clusters: pd.DataFrame, print_result: bool = True):
    validation_set = pd.read_csv(os.path.join('data', 'validation.csv'))
    validation_set = validation_set.merge(clusters[['url', 'smelly']], on='url')

    y_true = validation_set.final.to_list()
    y_pred = validation_set.smelly.to_list()
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    performance = {
        'precision': round(precision_score(y_true, y_pred), 4),
        'recall': round(recall_score(y_true, y_pred), 4),
        'mcc': round(matthews_corrcoef(y_true, y_pred), 4),
        'ari': round(adjusted_rand_score(y_true, y_pred), 4),
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn
    }

    if print_result:
        print('\n[PERFORMANCE] Performance relying on comparison with the validation dataset:')
        print(pd.DataFrame().append(performance, ignore_index=True).to_markdown(index=False, tablefmt="grid"))

    return performance
