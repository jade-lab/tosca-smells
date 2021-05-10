import json
import os
import pandas as pd
import yaml

try:
    relationships = pd.read_csv(os.path.join('data', 'relationships','relationship_types.csv'))
except FileNotFoundError:
    relationships = pd.DataFrame(columns=['node', 'smelly'])

with open(os.path.join('data', 'artifacts.json')) as f:
    artifacts = json.load(f)

    artifacts_count = 0
    for artifact in artifacts:
    
        artifacts_count += 1
        relationships_count = 0

        for node in artifact['relationship_types']:

            relationships_count += 1

            if str(node) in relationships.node.to_list():
                continue

            print(f'Still {len(artifacts) - artifacts_count} artifacts to go.')
            print(f'Still {len(artifact["relationship_types"]) - relationships_count} relationships in this artifact to analyse.')
            print('='*100)
            print(yaml.dump(node))
            print('='*100)
            smelly = input("Press Enter if NOT smelly\nType 'l'+Enter for Lazy Class.\nType 'u'+Enter for undeciced.\nType any other character + Enter if smelly.\nChoice: ")
            
            if smelly == '':
                relationships = relationships.append({'node': str(node), 'smelly': 'false'}, ignore_index=True)
            elif smelly == 'u':
                relationships = relationships.append({'node': str(node), 'smelly': 'unknown'}, ignore_index=True)
            elif smelly == 'l':
                relationships = relationships.append({'node': str(node), 'smelly': 'lazy'}, ignore_index=True)
            else:
                relationships = relationships.append({'node': str(node), 'smelly': 'true'}, ignore_index=True)
            
            os.system('clear')
        
        relationships.to_csv(os.path.join('data', 'relationships','relationship_types.csv'), index=False)
