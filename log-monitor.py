import pandas as pd
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from collections import Counter

# Load logs from CSV file
df_logs = pd.read_csv('sample_logs.csv')

df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
df_logs['text'] = df_logs['service'] + ' ' + df_logs['level'] + ' ' + df_logs['message']

model = SentenceTransformer('all-MiniLM-L6-v2')
df_logs['embedding'] = df_logs['text'].apply(lambda x: model.encode(x))
embeddings = np.vstack(df_logs['embedding'].values)
dbscan = DBSCAN(eps=0.5, min_samples=2, metric='euclidean')
df_logs['cluster'] = dbscan.fit_predict(embeddings)

df_logs['anomaly'] = df_logs['cluster'] == -1
cluster_counts = Counter(df_logs['cluster'])
df_logs['anomaly_score'] = df_logs['cluster'].apply(lambda x: 1 / cluster_counts[x] if x != -1 else 1)


anomalies = df_logs[df_logs['anomaly']]
print("Anomalous Logs:")
print(anomalies[['timestamp', 'text', 'anomaly_score']])

# Plotting anomaly scores
plt.figure(figsize=(12, 6))
plt.plot(df_logs['timestamp'], df_logs['anomaly_score'], marker='o', linestyle='-')
plt.xlabel('Timestamp')
plt.ylabel('Anomaly Score')
plt.title('Anomaly Scores Over Time')
plt.xticks(rotation=45)
plt.grid()
plt.show()
