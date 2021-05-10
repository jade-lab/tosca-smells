import json
import os
import pandas as pd
import yaml

try:
    interfaces = pd.read_csv(os.path.join('data', 'interfaces','interfaces.csv'))
except FileNotFoundError:
    interfaces = pd.DataFrame(columns=['interface', 'smelly'])

with open(os.path.join('data', 'artifacts.json')) as f:
    artifacts = json.load(f)

    artifacts_count = 0
    for artifact in artifacts:
    
        artifacts_count += 1
        interfaces_count = 0

        for interface in artifact['interfaces']:

            interfaces_count += 1

            if 'inputs:' not in yaml.dump(interface):
                continue

            if str(interface) in interfaces.interface.to_list():
                continue

            print(f'Still {len(artifacts) - artifacts_count} artifacts to go.')
            print(f'Still {len(artifact["interfaces"]) - interfaces_count} interfaces in this artifact to analyse.')
            print('='*100)
            print(yaml.dump(interface))
            print('='*100)
            smelly = input("Press Enter if NOT smelly\nType 'u'+Enter for undeciced.\nType any other character + Enter if smelly.\nChoice: ")
            
            if smelly == '':
                interfaces = interfaces.append({'interface': str(interface), 'smelly': 'false'}, ignore_index=True)
            elif smelly == 'u':
                interfaces = interfaces.append({'interface': str(interface), 'smelly': 'unknown'}, ignore_index=True)
            else:
                interfaces = interfaces.append({'interface': str(interface), 'smelly': 'true'}, ignore_index=True)
            
            os.system('clear')
        
        interfaces.to_csv(os.path.join('data', 'interfaces','interfaces.csv'), index=False)
