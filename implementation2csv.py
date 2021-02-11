import json
import os
import pandas as pd
import requests
import progressbar 

ansible_implementations = set()
py_implementations = set()
sh_implementations = set()
yml_implementations = set()
others_implementations = set()
 
  
widgets = [' [',  
    progressbar.Timer(format= 'elapsed time: %(elapsed)s'), '] ', 
    progressbar.Bar('*'),' (', 
    progressbar.ETA(), ') ', 
] 
  

with open(os.path.join('data', 'artifacts.json')) as f:
    artifacts = json.load(f)
    bar = progressbar.ProgressBar(max_value=len(artifacts), widgets=widgets).start()
    i = 1
    for artifact in artifacts:

        bar.update(i)
        i += 1

        if not artifact['implementations']:
            continue
        
        for url_to_imp in artifact['implementations']:
            if '/test' in url_to_imp:
                continue

            response = requests.get(url_to_imp)

            if response.status_code != 200:
                continue

            if url_to_imp.endswith('.yml') or url_to_imp.endswith('.yaml'):
                yml_implementations.add(url_to_imp)
            elif url_to_imp.endswith('.py'):
                py_implementations.add(url_to_imp)
            elif url_to_imp.endswith('.sh'):
                sh_implementations.add(url_to_imp)
            elif url_to_imp.endswith('.ansible'):
                ansible_implementations.add(url_to_imp)
            else:
                others_implementations.add(url_to_imp)

pd.DataFrame(ansible_implementations).to_csv(os.path.join('data', 'implementations','ansible.csv'), index=False)
pd.DataFrame(py_implementations).to_csv(os.path.join('data', 'implementations','python.csv'), index=False)
pd.DataFrame(sh_implementations).to_csv(os.path.join('data', 'implementations','sh.csv'), index=False)
pd.DataFrame(yml_implementations).to_csv(os.path.join('data', 'implementations','yaml.csv'), index=False)
pd.DataFrame(others_implementations).to_csv(os.path.join('data', 'implementations','others.csv'), index=False)
