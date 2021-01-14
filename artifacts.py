"""This module parse a blueprint to collect artifacts relevant for the code smell detection analysis.
   For example, NodeType, RelationshipType, Interfaces, and so forth.
"""


import json
import pandas as pd
import requests
import yaml


def get_node_types(d: dict):
    blueprint = d.copy()
    node_types = []

    while blueprint:
        key, item = blueprint.popitem()

        if key == 'node_types' and type(item) == dict:
            for k, v in item.items():
                node_types.append({k: v})

        elif type(item) == dict:
            blueprint.update(item)

    return node_types


def get_node_templates(d: dict):
    blueprint = d.copy()
    node_templates = []

    while blueprint:
        key, item = blueprint.popitem()

        if key == 'node_templates' and type(item) == dict:
            for k, v in item.items():
                node_templates.append({k: v})

        elif type(item) == dict:
            blueprint.update(item)

    return node_templates


def get_relationship_types(d: dict):
    blueprint = d.copy()
    relationship_types = []

    while blueprint:
        key, item = blueprint.popitem()

        if key == 'relationship_types' and type(item) == dict:
            for k, v in item.items():
                relationship_types.append({k: v})

        elif type(item) == dict:
            blueprint.update(item)

    return relationship_types


def get_relationship_templates(d: dict):
    blueprint = d.copy()
    relationship_templates = []

    while blueprint:
        key, item = blueprint.popitem()

        if key == 'relationship_templates' and type(item) == dict:
            for k, v in item.items():
                relationship_templates.append({k: v})

        elif type(item) == dict:
            blueprint.update(item)

    return relationship_templates


def get_interfaces(d: dict):
    blueprint = d.copy()
    interfaces_list = []

    while blueprint:
        key, item = blueprint.popitem()

        if key == 'interfaces' and type(item) == dict:
            for _, interfaces in item.items():
                if type(interfaces) == dict:
                    interfaces_list.extend([{k : v} for k, v in interfaces.items()])
                elif type(interfaces) == str:
                    print(interfaces)
        elif type(item) == dict:
            blueprint.update(item)

    return interfaces_list


def get_implementations(d: dict):
    interfaces = get_interfaces(d)
    implementations = set()

    for interface in interfaces:
        for k, v in interface.items():
            if type(v) == dict and 'implementation' in v.keys():
                try:
                    implementations.add(v['implementation'])
                except TypeError:
                    print(v)

            elif type(v) == str:
                implementations.add(v)

    return implementations


blueprints_df = pd.read_csv('data/tosca_blueprints.csv')

artifacts = []

for url_to_raw in blueprints_df.url_to_remote_raw.to_list():
    print(url_to_raw)

    response = requests.get(url_to_raw)

    if response.status_code != 200:
        continue

    try:
        blueprint = yaml.safe_load(response.content)
        if type(blueprint) != dict:
            continue

    except Exception:
        continue

    implementations_urls = []

    for path in get_implementations(blueprint):
        split_path = path.split('/')
        split_url = url_to_raw.split('/')

        if path.count('../') >= 1:
            split_url[-path.count('../')-1:] = split_path
        else:
            split_url[-1:] = split_path

        split_url = [i for i in split_url if i != '..']
        implementation_url = '/'.join(split_url)

        implementations_urls.append(implementation_url)

    artifacts.append({
        'blueprint': url_to_raw,
        'node_types': get_node_types(blueprint),
        'relationship_types': get_relationship_types(blueprint),
        'node_templates': get_node_types(blueprint),
        'relationship_templates': get_relationship_types(blueprint),
        'interfaces': get_interfaces(blueprint),
        'implementations': implementations_urls
    })


with open('artifacts.json', 'w') as f:
    json.dump(artifacts, f)
