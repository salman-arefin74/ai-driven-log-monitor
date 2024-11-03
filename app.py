from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import DBSCAN
from collections import Counter

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

import pandas as pd
df_logs = pd.read_csv('sample_logs.csv')
df_logs['text'] = df_logs['service'] + ' ' + df_logs['level'] + ' ' + df_logs['message']
df_logs['embedding'] = df_logs['text'].apply(lambda x: model.encode(x))
embeddings = np.vstack(df_logs['embedding'].values)

dbscan = DBSCAN(eps=0.5, min_samples=2, metric='euclidean')
df_logs['cluster'] = dbscan.fit_predict(embeddings)
cluster_counts = Counter(df_logs['cluster'])

class LogEntry(BaseModel):
    timestamp: str
    service: str
    level: str
    message: str

@app.post("/analyze_log/")
async def analyze_log(entry: LogEntry):
    full_message = f"{entry.service} {entry.level} {entry.message}"
    embedding = model.encode(full_message).reshape(1, -1)
    cluster = dbscan.fit_predict(embedding)
    anomaly_score = 1 if cluster[0] == -1 else 1 / cluster_counts[cluster[0]]
    is_anomaly = cluster[0] == -1

    return {"anomaly_score": anomaly_score, "is_anomaly": is_anomaly}
