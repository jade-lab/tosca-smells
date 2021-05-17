import json
import os
from io import StringIO
from collections import defaultdict
import time

import pandas as pd
import numpy as np
import requests
import yaml
from toscametrics.import_metrics import blueprint_metrics, general_metrics


def large_and_lazy_class_metrics(file_path: str = "data/tosca_blueprints.csv"):
    #Change this!!
    blueprints_df = pd.read_csv(file_path)[:100]

    metrics = {
        "num_properties": blueprint_metrics["num_properties"],
        "num_interfaces": blueprint_metrics["num_interfaces"]
    }


    for name, func in metrics.items():
        blueprints_df[name] = blueprints_df.apply(lambda row: calculate_tosca_metric(row["url_to_remote_raw"], func), axis=1)

    blueprints_df.to_csv("data/large_and_lazy_class_metrics.csv", index=False)



def long_method_metrics(file_path: str = "data/long_method.csv"):

    #Change this!!
    blueprints_df = pd.read_csv(file_path)[:100]

    blueprints_df["loc"] = blueprints_df.apply(lambda row: calculate_loc(row["url"]), axis=1)

    blueprints_df.to_csv("data/long_method_metrics.csv", index=False)



def calculate_tosca_metric(url, metric):
    response = requests.get(url)
    print(url)

    if response.status_code != 200:
        return "ERROR: File not found"

    try:
        blueprint = yaml.safe_load(response.content)
        if type(blueprint) != dict:
            return "ERROR: Type is not dict"

    except Exception:
        return "ERROR: Exception"

    return metric(response.content).count()


def calculate_loc(url):
    response = requests.get(url)
    print(url)

    if response.status_code != 200:
        return "ERROR: File not found"

    loc = 0

    for l in response.text.splitlines():
        if l.strip() and l.strip() != '---' and l.strip() != '-' and not l.strip().startswith('#'):
            loc = loc + 1
    return loc


large_and_lazy_class_metrics()
long_method_metrics()