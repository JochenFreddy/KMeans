# -*- coding: utf-8 -*-

!pip install kneed

import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

features, true_labels = make_blobs(
    n_samples=200,
    centers=3,
    cluster_std=2.75,
    random_state=42
)

features[:5]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

scaled_features[:5]

kmeans = KMeans(
    init= "random",
    n_clusters=3,
    n_init=10,
    max_iter = 300,
    random_state=42
)

kmeans.fit(scaled_features)

kmeans.cluster_centers_

kmeans_kwargs = {
    "init": "random",
    "n_init": 10,
    "max_iter": 300,
    "random_state": 42,
}

# A list holds the SSE values for each k
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    sse.append(kmeans.inertia_)

plt.style.use("fivethirtyeight")
plt.plot(range(1, 11), sse)
plt.xticks(range(1, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("SSE")
plt.show()

kl = KneeLocator(
    range(1,11),sse,curve= "convex",direction="decreasing"
)
kl.elbow

# A list holds the silhouette coefficients for each k
silhouette_coefficients = []

# Notice you start at 2 clusters for silhouette coefficient
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
    kmeans.fit(scaled_features)
    score = silhouette_score(scaled_features, kmeans.labels_)
    silhouette_coefficients.append(score)

plt.style.use("fivethirtyeight")
plt.plot(range(2, 11), silhouette_coefficients)
plt.xticks(range(2, 11))
plt.xlabel("Number of Clusters")
plt.ylabel("Silhouette Coefficient")
plt.show()

import tarfile
import urllib

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from google.colab import files
uploaded = files.upload()

import io
df2 = pd.read_csv(io.BytesIO(uploaded['Erta_Ale.csv']))

from google.colab import files
uploaded = files.upload()

df5 = pd.read_csv(io.BytesIO(uploaded['Nyiragongo.csv']))

from google.colab import files
uploaded = files.upload()

df6 = pd.read_csv(io.BytesIO(uploaded['Kilauea.csv']))

frames = [df2,df5,df6]
df2 = pd.concat(frames)

df2

#df3 = df2.loc[:, df2.columns != 'state']
df3 = df2
df3['p7/6'] = df3['p7']/df3['p6']
df3['p7/5'] = df3['p7']/df3['p5']
df3['p6/5'] = df3['p6']/df3['p5']
df3['S7'] = df3['p7']>10000
df3['S6'] = df3['p6']>10000
df3['b7'] = df3['p7']>1500
df3['b6'] = df3['p6'] >5000
df3['S7'] = df3['S7'].astype(int)
df3['S6'] = df3['S6'].astype(int)
df3['b7'] = df3['b7'].astype(int)
df3['b6'] = df3['b6'].astype(int)
df3

"""Test without PCA"""

from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df3)

kmeans = KMeans(n_clusters=9)
dbscan = DBSCAN(eps=0.3)

kmeans.fit(scaled_features)
dbscan.fit(scaled_features)

kmeans_silhouette = silhouette_score(
    scaled_features,kmeans.labels_
).round(2)
dbscan_silhouette = silhouette_score(
    scaled_features, dbscan.labels_
).round(2)

print(kmeans_silhouette)

print(dbscan_silhouette)

"""Test with PCA"""

def myplot(score, coeff, labels=None):
  xs = score[:,0]
  ys = score[:,1]
  n= coeff.shape[0]
  scalex = 1.0/(xs.max() - xs.min())
  scaley = 1.0/(ys.max() - ys.min())
  plt.scatter(xs * scalex, ys * scaley)
  for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
        if labels is None:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
        else:
            plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')
  plt.xlim(-1,1)
  plt.ylim(-1,1)
  plt.xlabel("PC{}".format(1))
  plt.ylabel("PC{}".format(2))
  plt.grid()

from sklearn.decomposition import PCA
import numpy as np
preprocessor = Pipeline(
    [
     ("scaler", MinMaxScaler()),
     ("pca", PCA(n_components = 2, random_state=42)),
    ]
)
my_model= PCA(n_components=2, random_state=42)
X_new = my_model.fit_transform(df3)
my_model.explained_variance_
my_model.explained_variance_ratio_
#my_model.explained_variance_ratio_.cumsum()
#abs(my_model.components_)

myplot(X_new[:,0:2], np.transpose(my_model.components_[0:2, :]))
plt.show()

label_encoder = LabelEncoder()
true_labels = label_encoder.fit_transform(df2.state)
label = df2.state.unique()
n_clusters = len(label)

clusterer = Pipeline(
    [
     (
         "kmeans",
      KMeans(
          n_clusters = 18,
          init="k-means++",
          n_init=100,
          max_iter = 500,
          random_state =None,
      ),
     ),
    ]
)

pipe = Pipeline(
    [("preprocessor", preprocessor),
     ("clusterer", clusterer)
     ]
)
pipe.fit(df3)

preprocessed_data = pipe["preprocessor"].transform(df3)

predicted_labels = pipe["clusterer"]["kmeans"].labels_

silhouette_score(preprocessed_data, predicted_labels)

adjusted_rand_score(true_labels,predicted_labels)

pcadf = pd.DataFrame(
    pipe["preprocessor"].transform(df3),
    columns=["component_1","component_2"],
)
pcadf["predicted_cluster"] = pipe["clusterer"]["kmeans"].labels_
pcadf["true_label"] = label_encoder.inverse_transform(true_labels)

cluster_map = pd.DataFrame()
cluster_map['data_index'] = df3.index.values
cluster_map['cluster'] = pipe["clusterer"]["kmeans"].labels_

plt.style.use("fivethirtyeight")
plt.figure(figsize=(8,8))

scat = sns.scatterplot(
    "component_1",
    "component_2",
    s=50,
    data=pcadf,
    hue="predicted_cluster",
    style="true_label",
    palette= "Set2",
)

scat.set_title(
    "Clustering results from Erta Ale Hotmap"
    )
plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad= 0.0)

plt.show()

df4 = df2.loc[:, df2.columns == 'state']
d = cluster_map[cluster_map.cluster == 4].join(df3,lsuffix=('3'), rsuffix='4')
occur = d.groupby(['state']).size()
display(occur)
d['p7'] = d['p7']/10000
d['p6'] = d['p6']/10000
d['p5'] = d['p5']/10000
d
boxplot = d.boxplot(column =['p7','p6','p5', 'p7/6','p7/5','p6/5'])
boxplot.set_ylim(0,7)

silhouette_scores= []
ari_scores = []
for n in range(2,11):
  pipe["preprocessor"]["pca"].n_components = n
  pipe.fit(df3)

  silhouette_coef = silhouette_score(
      pipe["preprocessor"].transform(df3),
      pipe["clusterer"]["kmeans"].labels_,
  )
  ari = adjusted_rand_score(
      true_labels,
      pipe["clusterer"]["kmeans"].labels_,
  )

  silhouette_scores.append(silhouette_coef)
  ari_scores.append(ari)

from sklearn import preprocessing
minmax_processed = preprocessing.MinMaxScaler().fit_transform(df3)
df_numeric_scaled = pd.DataFrame(minmax_processed, index=df3.index, columns=df3.columns[:])
df_numeric_scaled.head()

Nc = range(1, 20)

kmeans = [KMeans(n_clusters=i) for i in Nc]

score = [kmeans[i].fit(df_numeric_scaled).score(df_numeric_scaled) for i in range(len(kmeans))]

plt.plot(Nc,score)
plt.xlabel('Number of Clusters')
plt.ylabel('Score')
plt.title('Elbow Curve')
plt.show()

from IPython.core.pylabtools import figsize
plt.style.use("fivethirtyeight")
plt.figure(figsize=(6,6))
plt.plot(
    range(2,11),
    silhouette_scores,
    c="#008fd5",
    label="SC",
)
plt.plot(range(2,11), ari_scores, c="#fc4f30", label="ARI")

plt.xlabel("n_components")
plt.legend()
plt.title("Clustering performance for n_components")
plt.tight_layout()
plt.show()
