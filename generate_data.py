import numpy as np
import pandas as pd
from faker import Faker
from sklearn.cluster import AgglomerativeClustering
x = []
y = []
z = []
w = []
names = []
fake = Faker()
for _ in range(300):
  names.append(fake.name())
  x.append(np.random.randint(0, 10))
  y.append(np.random.randint(0, 10))
  z.append(np.random.randint(0, 10))
  w.append(np.random.randint(0, 10))


data = {"Extrovert - Introvert": x, "Sensing - Intuition": y, "Thinking - Feeling": z, "Judging - Perceiving": w}
df = pd.DataFrame(data)

neigh = AgglomerativeClustering(n_neighbors=3)
clustering = AgglomerativeClustering().fit(data)


print(df)

