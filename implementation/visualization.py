import pandas as pd
import matplotlib.pyplot as plt


from sklearn.preprocessing import normalize, MinMaxScaler
from sklearn.cluster import AgglomerativeClustering
import scipy
from scipy.cluster import hierarchy

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler



large_class_df = pd.read_csv('implementation/metrics/large_class.csv')
# large_class_df.hist()

# X, Y = large_class_df[['lines_code', 'num_interfaces', 'num_properties', 'num_tokens', 'entropy']], large_class_df.smelly
X, Y = large_class_df[['lines_code', 'num_interfaces', 'num_properties']], large_class_df.smelly
print(X.columns)

print(X.shape)
print(Y.to_list().count(1))

# X, Y = RandomOverSampler(random_state=0, sampling_strategy='minority').fit_resample(X, Y)
X, Y = RandomUnderSampler(random_state=0, sampling_strategy='majority').fit_resample(X, Y)
print(X.shape)

X['smelly'] = Y
print(X[X.smelly == True])
# print(Y.to_list().count(1))
# Normalize by lines of code
# X = X.div(X.lines_code, axis=0)
# X = X.drop(['lines_code'], axis=1).to_numpy()
X = X.to_numpy()

fig = plt.figure()
ax = plt.axes(projection="3d")

z_points = X[:, 0]
x_points = X[:, 1]
y_points = X[:, 2]
colors = []

for item in Y.ravel():
    if item == 0:
        colors.append('grey')
    else:
        colors.append('r')

ax.scatter3D(x_points, y_points, z_points, c=colors, cmap='hsv')
ax.set_xlabel('Num properties')
ax.set_ylabel('Num interfaces')
ax.set_zlabel('LOC')
plt.show()

#
# X, Y = large_class_df[['num_interfaces', 'num_properties']], large_class_df.smelly
#
#
# X = pd.DataFrame(X.sum(axis=1))
# X_norm = MinMaxScaler().fit_transform(X) #X.to_numpy()
# print(X_norm)
# plt.scatter(range(0, len(X_norm[:, 0])), X_norm[:, 0], c=Y)
# plt.show()
