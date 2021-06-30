import os
import numpy as np
import pandas as pd
import scipy.stats as stats

from sklearn.metrics import confusion_matrix, matthews_corrcoef, precision_score, recall_score
from sklearn.preprocessing import RobustScaler

from statsmodels.stats.outliers_influence import variance_inflation_factor


def reduce_multicollinearity(df: pd.DataFrame, threshold: int = 10):
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

    print(f'\n[MULTICOLLINEARITY REDUCTION] Metrics removed from the dataset as result of multicollinearity reduction '
          f'(VIF > {threshold}):')
    print(vif_results.to_markdown(index=False, tablefmt="grid"))


def normalize(df: pd.DataFrame):
    columns = df.columns
    normalizer = RobustScaler()
    return normalizer, pd.DataFrame(normalizer.fit_transform(df), columns=columns)


def cohen_d(d1, d2):
    # calculate the size of samples
    n1, n2 = len(d1), len(d2)
    # calculate the variance of the samples
    s1, s2 = np.var(d1, ddof=1), np.var(d2, ddof=1)
    # calculate the pooled standard deviation
    s = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    # calculate the means of the samples
    u1, u2 = np.mean(d1), np.mean(d2)
    # calculate the effect size
    return (u1 - u2) / s


def statistical_analysis(cluster_smelly: pd.DataFrame, cluster_sound: pd.DataFrame):

    if 'url' in cluster_smelly.columns:
        cluster_smelly.drop(['url'], axis=1, inplace=True)
    if 'cluster_id' in cluster_smelly.columns:
        cluster_smelly.drop(['cluster_id'], axis=1, inplace=True)
    if 'smelly' in cluster_smelly.columns:
        cluster_smelly.drop(['smelly'], axis=1, inplace=True)

    stat_results = pd.DataFrame()
    n_tests = cluster_smelly.columns.size

    for feature in cluster_smelly.columns:

        u_stat, p_value = stats.mannwhitneyu(cluster_smelly[feature], cluster_sound[feature], alternative='greater')
        d = cohen_d(cluster_smelly[feature], cluster_sound[feature])

        if p_value * n_tests < 0.01:
            stat_results = stat_results.append({
                'feature': feature.upper(),
                'p-value': p_value,
                'p-value corrected': p_value * n_tests,
                'U': u_stat,
                'cohen_d': d,
                'mean smelly': round(np.mean(cluster_smelly[feature])),
                'mean sound': round(np.mean(cluster_sound[feature]))
            }, ignore_index=True)

    print(f'\n[STATISTICAL ANALYSIS] Results of the statistical analysis with {n_tests} comparisons and a corrected '
          f'significance level alpha = {round(0.01 / n_tests, 4)} according to Bonferroni\'s correction:')
    print(stat_results.to_markdown(index=False, tablefmt="grid"))


def calculate_performance(clusters: pd.DataFrame):
    validation_set = pd.read_csv(os.path.join('data', 'validation.csv'))
    validation_set = validation_set.merge(clusters[['url', 'smelly']], on='url')

    y_true = validation_set.final.to_list()
    y_pred = validation_set.smelly.to_list()
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    performance = pd.DataFrame()
    performance = performance.append({
        'precision': round(precision_score(y_true, y_pred), 4),
        'recall': round(recall_score(y_true, y_pred), 4),
        'mcc': round(matthews_corrcoef(y_true, y_pred), 4),
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn
    }, ignore_index=True)

    print('\n[PERFORMANCE] Performance relying on comparison with the validation dataset:')
    print(performance.to_markdown(index=False, tablefmt="grid"))
