# README

This is the replication package for the paper: **A Large Empirical Study on Blob Blueprint in Technology-Agnostic Infrastructure Code**.


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

Follow the instructions in the terminal to run the desired experiment and plot graphs.



## Additional information

* `data/tosca_repositories.csv` is a static file containing the collected TOSCA repositories.


* `data/tosca_blueprints.csv` is generated running `python clustering/collect_blueprints.py`. That script collects the raw urls of 
  blueprints in the latest release of every repository. Use this command if you want to collect updated blueprints.   


* `data/metrics.csv` is generated running `python clustering/collect_metrics.py`. That script uses the previous csv to access the 
  raw content of every blueprint and extract the metrics used in this study.

* `data/validation.csv` is a static file containing the validation results among the assessors.  

* `data/EXPLORATORY_ANALYSIS.md/` contains results for **RQ1**.

* `data/performance/` and `STATISTICAL_ANALYSIS.md` contains results of the empirical evaluation for **RQ2**.  

* `data/feature-selection/` contains results of the stepwise forward selection for **RQ3**.

