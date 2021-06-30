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

    if 'example' in row['url']:
        continue

    response = requests.get(row['url'])

    if response.status_code == 200:

        try:
            extracted_metrics = extract_all(response.content.decode())
        except TypeError:
            continue
        except Exception as e:
            print(e)

        if all(value == 0 for value in extracted_metrics.values()):
            continue

        for key in list(extracted_metrics):
            if key not in ('lines_code',
                           'num_interfaces',
                           'num_properties',
                           'num_imports',
                           'num_node_templates', 'num_node_types',
                           'num_relationship_templates', 'num_relationship_types',
                           'num_capabilities',
                           'num_requirements',
                           'num_inputs',
                           'num_keys',
                           'num_suspicious_comments',
                           'num_tokens',
                           'lcot',
                           'text_entropy'):

                del extracted_metrics[key]

        extracted_metrics.update({'url': row['url']})

        metrics = metrics.append(extracted_metrics, ignore_index=True)

    metrics.to_csv(os.path.join('data', 'metrics.csv'), index=False)
