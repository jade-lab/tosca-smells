"""Usage:

python validate.py path/to/output/folder

"""

import os
import pandas as pd
import requests
import sys
import yaml

from screen import Screen

def main():

    paths = {
        '1': os.path.join(sys.argv[1], 'long_method.csv'),
        '2': os.path.join(sys.argv[1], 'large_class.csv'),
        '3': os.path.join(sys.argv[1], 'lazy_class.csv'),
    }

    choice = input('Press (1) for validating Long Method; (2) for Large Class; (3) for Lazy Class: ')       
    
    if choice.lower() == '1':
        dataset = pd.read_csv('long_method.csv')
    elif choice.lower() == '2':
        dataset = pd.read_csv('large_class.csv')
    elif choice.lower() == '3':
        dataset = pd.read_csv('lazy_class.csv')
    else:
        print('Invalid choice.')
        exit()

    idx_from = int(input(f'From csv index (max {dataset.shape[0]-1}): '))
    idx_to = int(input(f'To csv index (max {dataset.shape[0]-1}): '))

    for idx, row in dataset.iterrows():
        
        if type(row.smelly) == bool or idx < idx_from:
            continue

        if choice.lower() == '1':
            response = requests.get(row.url)
            if response.status_code != 200:
                continue
            else:
                text = response.text
                smell = 'Long Method'
        elif choice.lower() == '2':
            text = yaml.dump(yaml.safe_load(row.type))
            smell = 'Large Class'
        elif choice.lower() == '3':
            text = yaml.dump(yaml.safe_load(row.type))
            smell = 'Lazy Class'

        lines = [f'{idx_to-idx_from} artifacts to go', 'Scroll text using ( ↓ | ↑ | → | ← ) - Press ESC to quit', '', '']
        lines.extend(text.splitlines())
        lines.extend(['', '', f'Press Enter if NOT {smell.upper()} or any other character if {smell.upper()}: '])
        sc = Screen(lines)
        ch = sc.run()

        if ch == 27:  # 27 = ESC
            print('Bye!')
            exit()

        dataset.loc[idx, 'smelly'] = ch != 10  # 10 is key: ENTER        
        dataset.to_csv(paths[choice.lower()], index=False)

        if idx == idx_to:
            print('Validation completed. Thank you!')
            exit()

if __name__ == '__main__':
    main()

