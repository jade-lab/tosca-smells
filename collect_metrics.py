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

        extracted_metrics = extract_all(response.content.decode())
        if all(value == 0 for value in extracted_metrics.values()):
            continue

        extracted_metrics.update({'url': row['url']})

        if 'lines_blank' in extracted_metrics:
            del extracted_metrics['lines_blank']

        if 'lines_comment' in extracted_metrics:
            del extracted_metrics['lines_comment']

        metrics = metrics.append(extracted_metrics, ignore_index=True)

    metrics.to_csv(os.path.join('data', 'metrics.csv'), index=False)
