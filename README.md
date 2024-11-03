# Log Monitor

This log monitoring system uses Large Language Model (LLM)-based embeddings and DBSCAN clustering to detect anomalies in microservice logs. The goal is to identify abnormal log entries—such as errors, warnings, or unexpected behavior—that may indicate issues in the system.

## How LLM is Used

The LLM is used to generate embeddings (dense vector representations) for each log entry. These embeddings capture the semantic meaning of each log message, enabling the system to identify patterns and similarities between different logs. For example:

* Log entries like "Request received at /api/v1/user" and "Request received at /api/v1/orders" will have similar embeddings because their meanings are close.
* Errors like "Memory overflow in image processing service" will have embeddings different from typical informational logs, as they indicate an issue rather than routine activity.

## Anomaly Detection with DBSCAN

Once the embeddings are created, I used DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to group similar logs into clusters. This process works as follows:

* Clustering: DBSCAN groups logs with similar embeddings into clusters, treating these as normal behavior.
* Noise Identification: Logs that don't fit into any cluster are marked as noise or anomalies. These logs are considered abnormal due to their semantic dissimilarity from normal patterns.

For example,

* Logs with typical messages like Request received at `/api/v1/user` and `Database connection established` will cluster together.
* Anomalies, such as `Timeout error during request processing` and `Memory overflow in image processing service`, are not similar to regular logs, so they don’t belong to any cluster. DBSCAN flags these as anomalies.

## Examples of Anomalous and Normal Logs

With DBSCAN, we can differentiate logs as follows:

* Normal Logs (clustered together):
    [INFO] Request received at /api/v1/user
    [INFO] Request processed successfully
    [DEBUG] Connecting to database
* Anomalous Logs (identified as noise):
    [ERROR] Memory overflow in image processing service
    [WARNING] Slow response from backend service
    [ERROR] Timeout error during request processing

## How to Run and Test the System
1. Ensure you have Python and necessary packages installed:
```
bash

pip install numpy pandas sklearn sentence-transformers
```

2. Save your logs in a CSV file named `sample_logs.csv` with the following format:
```
log_level,timestamp,message
INFO,2024-11-03T10:00:23,Request received at /api/v1/user
DEBUG,2024-11-03T10:00:25,Connecting to database
...
```

3. Place the following files in the same directory:

* log_monitor.py: This file contains the main code for the LLM-based embedding and DBSCAN clustering.
* app.py: This is the entry point to process the logs, apply DBSCAN, and print out detected anomalies.

4. Run `python app.py`
