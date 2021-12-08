# README

This is the replication package for the paper: **Detecting Technology-Agnostic Infrastructure Code Smells Using Unsupervised Learning: a Case Study on Large Class**.

Below some useful information to replicate the work.

<p align="center" width="100%">
    <img src="./pipeline.png"> 
</p>

## How to reproduce

* **(Optional)** Create a virtual environment:
```commandline
virtualenv venv
source venv/bin/activate
```

* Install dependencies and run the program:
```commandline
pip install -r requirements.txt
python main.py
```

Follow the instructions in the terminal to run the desired experiment.



## Additional information

* `data/tosca_repositories.csv` is a static file containing the collected TOSCA repositories.


* `data/tosca_blueprints.csv` is generated running `python clustering/collect_blueprints.py`. That script collects the raw urls of 
  blueprints in the latest release of every repository. Use this command if you want to collect updated blueprints.   


* `data/metrics.csv` is generated running `python clustering/collect_metrics.py`. That script uses the previous csv to access the 
  raw content of every blueprint and extract the metrics used in this study.


* `data/clusters.csv` is generated running `python clustering/clustering.py`. That is the only script that has to be run to
  replicate the study. In addition, it shows information about the statistical analysis.
  

* `data/clusters_additional.csv` is generated running `python clustering/clustering_additional.py`. That script shows information 
  about the additional analysis performed by normalizing all the metrics by the lines of code.


* `data/clusters_loc.csv` is generated running `python clustering/clustering_loc.py`. That script shows information about the 
  additional analysis performed using the metrics LinesCode solely.

* `data/clusters_significant_metrics.csv` is generated running `python clustering/clustering_significant_metrics.py`. That script shows information about the 
  additional analysis performed using the metrics that distribute significantly differently between the clusters.


* `data/validation.csv` is a static file containing the validation results among the assessors.  

