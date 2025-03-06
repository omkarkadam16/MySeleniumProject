import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_csv("test_logs.csv")
model = KMeans(n_clusters=3)
df["Cluster"] = model.fit_predict(df[["execution_time", "error_count"]])

print(df.head())
