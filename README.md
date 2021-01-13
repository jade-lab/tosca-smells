# tosca-smells
Tosca smells...

- **blueprints.csv** - blueprints collected from ~650 TOSCA-based repositories on Github.
- **artifacts.xxx** - containing the blueprints components to compute the smell detection on (e.g., node types for Large/Lazy CLass smell; interfaces+implementations for Long Parameter List and Long Method smell).
- **labeled_dataset.csv** - |id component (linked to artifacts.xxx)|m1|m2|m3...|smell {none, Lazy, Large...}
