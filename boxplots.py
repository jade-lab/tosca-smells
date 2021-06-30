import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler

metrics_df = pd.read_csv('data/metrics.csv')
# metrics_df = metrics_df.merge(
#     pd.read_csv('data/validation.csv')[['url', 'final']],
#     on='url').drop(['url'], axis=1)
# metrics_df.rename(columns = {'final':'smelly'}, inplace = True)

metrics_df = metrics_df.merge(
    pd.read_csv('data/clusters_significant_metrics_kmeans.csv')[['url', 'smelly']],
    on='url').drop(['url'], axis=1)

metrics_df = metrics_df[['lines_code', 'num_capabilities', 'num_interfaces', 'num_node_types', 'num_properties',
                         'num_relationship_types', 'num_requirements', 'num_suspicious_comments', 'text_entropy',
                         'smelly']]

X = metrics_df.drop(['smelly'], axis=1)
y = metrics_df.smelly

columns = X.columns
metrics_df = pd.DataFrame(MinMaxScaler().fit_transform(X, y), columns=columns)
metrics_df['smelly'] = y

# Normalize by lines of code
# smelly = metrics_df['smelly']
# metrics_df.drop(['smelly'], axis=1, inplace=True)
# metrics_df = metrics_df.div(metrics_df.lines_code, axis=0)
# metrics_df.drop(['lines_code'], axis=1, inplace=True)
# metrics_df['smelly'] = smelly

data_to_plot = pd.DataFrame(columns=['value', 'measure', 'smelly'])

for _, row in metrics_df.iterrows():

    for column in set(metrics_df.columns) - {'smelly', 'num_suspicious_comments'}:
        data_to_plot = data_to_plot.append({
            'measure': column,
            'value': row[column],
            'smelly': row['smelly'],
        }, ignore_index=True)

sns.set_theme(style="whitegrid")
ax = sns.boxplot(x="measure", y="value", hue="smelly", data=data_to_plot, palette="Set3")
plt.show()
