import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

large_class_df = pd.read_csv('implementation/metrics/large_class.csv')
large_class_df.drop_duplicates(inplace=True)

target = large_class_df.smelly

large_class_df.drop(['smelly'], axis=1, inplace=True)
feature_names = large_class_df.columns.to_list()

large_class_df = StandardScaler().fit_transform(large_class_df)
large_class_df = pd.DataFrame(large_class_df, columns=feature_names)

tsne = TSNE(random_state=0)
tsne_results = tsne.fit_transform(large_class_df)

tsne_results=pd.DataFrame(tsne_results, columns=['tsne1', 'tsne2'])

plt.scatter(tsne_results['tsne1'], tsne_results['tsne2'], c=target)
plt.show()
