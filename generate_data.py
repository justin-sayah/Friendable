import numpy as np
import pandas as pd
from faker import Faker
from sklearn.cluster import KMeans
from joblib import dump, load

x = []
y = []
z = []
w = []
cereal = []
hotdog = []
sleep = []
ice_cream = []
messy = []
aliens = []

names = []
fake = Faker()
for _ in range(1500):
  names.append(fake.name())
  x.append(np.round(np.random.uniform(1, 10),2))
  y.append(np.round(np.random.uniform(1, 10),2))
  z.append(np.round(np.random.uniform(1, 10),2))
  w.append(np.round(np.random.uniform(1, 10),2))
  cereal.append(np.random.randint(3))
  hotdog.append(np.random.randint(3))
  sleep.append(np.random.randint(3))
  ice_cream.append(np.random.randint(3))
  messy.append(np.random.randint(3))
  aliens.append(np.random.randint(3))



data = {"Name":names,"EF": x, "SI": y, "TF": z, "JP": w, "Cereal": cereal,
 "Hotdog":hotdog, "Sleep": sleep, "IceCream": ice_cream, "Messy": messy, "Aliens":aliens}
df = pd.DataFrame(data)

kmeans = KMeans(n_clusters=30, random_state=0).fit(df.iloc[:, 1:11])
dump(kmeans, 'kmeans_model.joblib') 
labels = kmeans.labels_

df["Classes"] = pd.Series(labels)

print(labels)
# neigh = AgglomerativeClustering(n_neighbors=3)
# clustering = AgglomerativeClustering().fit(data)
df.to_csv("fake_people.csv", index = False)

print(df)

test = np.array([2.5,6.4, 9.7, 2.1,0,0, 1, 0, 0,1])
test.reshape(-1,1)
prediction = kmeans.predict([test])

print(prediction)
