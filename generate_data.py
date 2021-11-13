import numpy as np
import pandas as pd
from faker import Faker
from sklearn.cluster import AgglomerativeClustering
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
for _ in range(300):
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


data = {"EF": x, "SI": y, "TF": z, "JP": w, "Cereal": cereal,
 "Hotdog":hotdog, "Sleep": sleep, "Ice Cream": ice_cream, "Messy": messy, "Aliens":aliens}
df = pd.DataFrame(data)

# neigh = AgglomerativeClustering(n_neighbors=3)
# clustering = AgglomerativeClustering().fit(data)


print(df)

