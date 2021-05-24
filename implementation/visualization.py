import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits import mplot3d

from sklearn.preprocessing import normalize, MinMaxScaler
from sklearn.cluster import AgglomerativeClustering
import scipy
from scipy.cluster import hierarchy


large_class_df = pd.read_csv('implementation/large_class_metrics.csv').drop(['type'], axis=1)
# large_class_df.hist()

# X, Y = large_class_df[['lines_code', 'num_interfaces', 'num_properties', 'entropy']], large_class_df.smelly
X, Y = large_class_df[['num_interfaces', 'num_properties']], large_class_df.smelly


X = pd.DataFrame(X.sum(axis=1))
X_norm = MinMaxScaler().fit_transform(X) #X.to_numpy()
print(X_norm)
plt.scatter(range(0, len(X_norm[:, 0])), X_norm[:, 0], c=Y)
plt.show()
exit()
# plt.scatter(X_norm[:, 0], X_norm[:, 1], c=Y)
# plt.xlabel(X.columns[0])
# plt.ylabel(X.columns[1])


# Normalize by lines of code
# X = X.div(X.lines_code, axis=0)
# X = X.drop(['lines_code'], axis=1).to_numpy()

# fig = plt.figure()
# ax = plt.axes(projection="3d")
#
# z_points = X_norm[:, 1]
# x_points = X_norm[:, 2]
# y_points = X_norm[:, 3]
# ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv')
#
# plt.show()

# for i in range(0,3):
#     for j in range(i+1,3):
#         plt.scatter(X_norm[:, i], X_norm[:, j], c=Y)
#         plt.xlabel(X.columns[i])
#         plt.ylabel(X.columns[j])
#         plt.title("Large Class Dataset")
#         plt.show()
