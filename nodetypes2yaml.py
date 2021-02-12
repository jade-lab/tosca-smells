import json
import os
import pandas as pd
import yaml

try:
    nodes = pd.read_csv(os.path.join('data', 'nodes','node_types.csv'))
except FileNotFoundError:
    nodes = pd.DataFrame(columns=['node', 'smelly'])

with open(os.path.join('data', 'artifacts.json')) as f:
    artifacts = json.load(f)

    artifacts_count = 0
    for artifact in artifacts:
    
        artifacts_count += 1
        nodes_count = 0

        for node in artifact['node_types']:

            nodes_count += 1

            if str(node) in nodes.node.to_list():
                continue

            print(f'Still {len(artifacts) - artifacts_count} artifacts to go.')
            print(f'Still {len(artifact["node_types"]) - nodes_count} nodes in this artifact to analyse.')
            print('='*100)
            print(yaml.dump(node))
            print('='*100)
            smelly = input("Press Enter if NOT smelly\nType 'l'+Enter for Lazy Class.\nType 'u'+Enter for undeciced.\nType any other character + Enter if smelly.\nChoice: ")
            
            if smelly == '':
                nodes = nodes.append({'node': str(node), 'smelly': 'false'}, ignore_index=True)
            elif smelly == 'u':
                nodes = nodes.append({'node': str(node), 'smelly': 'unknown'}, ignore_index=True)
            else:
                nodes = nodes.append({'node': str(node), 'smelly': 'true'}, ignore_index=True)
            
            os.system('clear')
        
        nodes.to_csv(os.path.join('data', 'nodes','node_types.csv'), index=False)
