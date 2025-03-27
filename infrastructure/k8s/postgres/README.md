# PostgreSQL on Minikube Setup Guide

This guide explains how to deploy PostgreSQL on Minikube and populate it with sample data.

## Prerequisites

- Minikube installed and running
- kubectl CLI installed
- psql client installed

## Deployment Steps

1. Start Minikube if not already running:
```bash
minikube start

kubectl apply -f namespace.yaml

kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f storage.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

2. Verify the deployment:


```bash
kubectl get pods -n data-platform
kubectl get services -n data-platform
```


## Connecting to PostgreSQL

1. Forward the postgreSQL port to your local machine

```bash
kubectl port-forward -n data-platform svc/postgres 5432:5432
```

2. Connect to PostgreSQL using psql

```bash
psql -h localhost -p 5432 -U etluser -d etldb
```