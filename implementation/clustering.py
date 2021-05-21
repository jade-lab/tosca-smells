import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import MinMaxScaler


def smell_clustering(path: str, feature_columns: list, smell: str):
    blueprints_df = pd.read_csv(path)
    print("Train df size: ", blueprints_df.shape)
    print(
        "number of rows with nan: ",
        blueprints_df[blueprints_df.isna().any(axis=1)].shape[0],
    )
    print("Train before scaling:", blueprints_df.describe())

    # Delete NaN rows
    blueprints_df = blueprints_df.dropna(subset=feature_columns)

    # Scale/normalize?
    scaler = MinMaxScaler()
    blueprints_df[feature_columns] = scaler.fit_transform(
        blueprints_df[feature_columns]
    )

    # Sum for label determination
    blueprints_df["metrics_sum"] = blueprints_df.loc[:, feature_columns].sum(axis=1)

    # Aglo
    agglo_model = AgglomerativeClustering(n_clusters=2)
    blueprints_df["agglo_labels"] = agglo_model.fit_predict(
        blueprints_df[feature_columns]
    )

    # GM
    gm_model = GaussianMixture(n_components=2)
    blueprints_df["gm_labels"] = gm_model.fit_predict(blueprints_df[feature_columns])

    # Kmeans
    kmeans_model = KMeans(n_clusters=2)
    blueprints_df["kmeans_labels"] = kmeans_model.fit_predict(
        blueprints_df[feature_columns]
    )

    # assign with cluster is smelly or not
    blueprints_df = label_determination(
        blueprints_df, feature_columns, "agglo_labels", smell
    )
    blueprints_df = label_determination(
        blueprints_df, feature_columns, "gm_labels", smell
    )
    blueprints_df = label_determination(
        blueprints_df, feature_columns, "kmeans_labels", smell
    )

    blueprints_df.to_csv(f"{smell}_clustered.csv", index=False)


def label_determination(blueprints_df, feature_columns, label_column, smell):

    label_zero_average = blueprints_df[blueprints_df[label_column] == 0][
        "metrics_sum"
    ].mean()
    label_one_average = blueprints_df[blueprints_df[label_column] == 1][
        "metrics_sum"
    ].mean()
    print("label zero: ", label_zero_average)
    print("label one: ", label_one_average)

    if (
        smell == "large_class" or smell == "long_method"
    ) and label_zero_average > label_one_average:
        blueprints_df[label_column] = np.where(
            (blueprints_df[label_column] == 0), "smelly", "sound"
        )

    elif (
        smell == "large_class" or smell == "long_method"
    ) and label_zero_average < label_one_average:
        blueprints_df[label_column] = np.where(
            (blueprints_df[label_column] == 1), "smelly", "sound"
        )

    elif smell == "lazy_class" and label_zero_average > label_one_average:
        blueprints_df[label_column] = np.where(
            (blueprints_df[label_column] == 1), "smelly", "sound"
        )

    elif smell == "lazy_class" and label_zero_average < label_one_average:
        blueprints_df[label_column] = np.where(
            (blueprints_df[label_column] == 0), "smelly", "sound"
        )
    else:
        blueprints_df[label_column] = "equal"

    return blueprints_df


large_lazy_class_feature_columns = [
    "lines_code",
    "lines_blank",
    "lines_comment",
    "num_keys",
    "num_suspicious_comments",
    "num_tokens",
    "text_entropy",
    "num_imports",
    "num_inputs",
    "num_interfaces",
    "num_node_templates",
    "num_node_types",
    "num_parameters",
    "num_properties",
    "num_relationship_templates",
    "num_relationship_types",
    "num_shell_scripts",
]
long_method_feature_columns = ["lines_code"]

smell_clustering(
    "large_class.csv",
    large_lazy_class_feature_columns,
    "large_class",
)
smell_clustering(
    "lazy_class.csv",
    large_lazy_class_feature_columns,
    "lazy_class",
)
smell_clustering("long_method.csv", long_method_feature_columns, "long_method")
