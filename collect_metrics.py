import os
import pandas
import requests

from toscametrics.metrics_extractor import extract_all

blueprints = pandas.read_csv(os.path.join('data', 'tosca_blueprints.csv'))
metrics = pandas.DataFrame()

i = 0
for _, row in blueprints.iterrows():

    i += 1
    print(f'({i}/{blueprints.shape[0]}) Collecting metrics for', row['url'])

    if 'examples/' in row['url']:
        continue

    response = requests.get(row['url'])

    if response.status_code == 200:
        extracted_metrics = {'url': row['url']}
        extracted_metrics.update(extract_all(response.content.decode()))
        del extracted_metrics['lines_blank', 'lines_comment']

        metrics = metrics.append(extracted_metrics, ignore_index=True)

    metrics.to_csv(os.path.join('data', 'metrics.csv'), index=False)
