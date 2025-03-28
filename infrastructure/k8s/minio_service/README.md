# MinIO Setup Guide

This guide explains how to deploy and access MinIO on Minikube.

## Prerequisites

- Minikube cluster running
- kubectl CLI installed
- Python with boto3 package (for data upload)

## Deployment Steps

1. Create the required directory in Minikube:
```bash
minikube ssh
sudo mkdir -p /data/minio
sudo chmod 777 /data/minio
exit
```

2. Deploy MinIO services:
```bash
kubectl apply -f storage.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

3. Verify the deployment:
```bash
kubectl get pods -n data-platform -l app=minio
kubectl get services -n data-platform | grep minio
```

## Accessing MinIO

### Console UI Access

1. Get the MinIO service URL:
```bash
minikube service minio -n data-platform --url
```

2. Access the Console UI:
- Use the URL with port 9001 from the previous command
- Default credentials:
  - Username: `minioadmin`
  - Password: `minioadmin`

Alternatively, use port-forwarding:
```bash
kubectl port-forward -n data-platform svc/minio 9001:9001
```
Then access: http://localhost:9001

### API Access

For programmatic access, use port-forwarding:
```bash
kubectl port-forward -n data-platform svc/minio 9000:9000
```

## Sample Data Upload

Use the miniIO UI or by script

## Troubleshooting

1. Check pod status:
```bash
kubectl describe pod -n data-platform -l app=minio
```

2. View pod logs:
```bash
kubectl logs -n data-platform -l app=minio
```

3. Verify storage:
```bash
kubectl get pv | grep minio
kubectl get pvc -n data-platform | grep minio
```

## MinIO Client (mc) Setup

1. Install MinIO Client:
```bash
brew install minio/stable/mc
```

2. Configure MinIO Client:
```bash
mc alias set local-minio http://localhost:9000 minioadmin minioadmin
```

3. Test connection:
```bash
mc ls local-minio
```

## Default Credentials

- Access Key: `minioadmin`
- Secret Key: `minioadmin`

Note: For production use, change default credentials and implement proper security measures.
Also if you don't forward the ports for local use you can't rech you minio bucket