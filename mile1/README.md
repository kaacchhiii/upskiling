# Mile 1 — Production-Grade Kubernetes Multi-Tier App

A 3-tier application running on Kubernetes with autoscaling, network policies, observability, and security scanning.

## Architecture

```
User → Frontend (nginx:80) → Backend (Flask:8000) → PostgreSQL (5432)
                                                      ↑
                                        Prometheus scrapes all tiers
                                        Grafana dashboards
```

## Tech Stack

| Tier       | Image              | Purpose                    |
|------------|--------------------|----------------------------|
| Frontend   | nginx:1.27-alpine  | Reverse proxy, serves UI   |
| Backend    | Flask (Python)     | REST API                   |
| Database   | postgres:16-alpine | Data storage (StatefulSet) |
| Monitoring | kube-prometheus-stack | Metrics + dashboards     |

## Quick Start

```bash
# 1. Create namespace
kubectl apply -f k8s/namespace.yaml

# 2. Deploy database
kubectl apply -f k8s/database/

# 3. Build and deploy backend
docker build -t mile1-backend:latest apps/backend/
kubectl apply -f k8s/backend/

# 4. Deploy frontend
kubectl apply -f k8s/frontend/

# 5. Apply network policies
kubectl apply -f k8s/network-policies/

# 6. Deploy monitoring (requires Helm)
bash k8s/monitoring/deploy.sh
```

## Verify It Works

```bash
# Check all pods are running
kubectl get pods -n app

# Test the backend API
kubectl port-forward svc/backend 8000:8000 -n app
curl http://localhost:8000/health
curl http://localhost:8000/api/items
curl -X POST http://localhost:8000/api/items -H "Content-Type: application/json" -d '{"name":"test"}'

# Access Grafana
kubectl port-forward svc/kube-prometheus-grafana 3000:80 -n monitoring
# Open http://localhost:3000 (admin / admin)
```

## What's In This Project

| Feature             | Where                        | What It Does                                    |
|---------------------|------------------------------|-------------------------------------------------|
| Multi-tier app      | `k8s/frontend/`, `backend/`, `database/` | 3 tiers talking through Services       |
| Autoscaling         | HPA in frontend + backend    | Scales pods up/down based on CPU                |
| Network policies    | `k8s/network-policies/`      | Deny-by-default, allow only needed traffic      |
| Observability       | `k8s/monitoring/`            | Prometheus + Grafana + alerts                   |
| Security scanning   | `.github/workflows/`         | Trivy scans images, manifests, and dependencies |
| Persistent storage  | Database StatefulSet + PVC   | Data survives pod restarts                      |
| Secrets             | K8s Secret for DB creds      | Credentials not hardcoded in manifests          |
| Health checks       | Liveness + readiness probes  | K8s knows when pods are healthy                 |
| Resource limits     | All deployments              | Prevents pods from consuming too many resources |

## Project Structure

```
mile1/
├── apps/backend/                    # Flask API source code + Dockerfile
├── k8s/
│   ├── namespace.yaml               # "app" namespace
│   ├── frontend/deployment.yaml     # nginx + config + service + HPA
│   ├── backend/deployment.yaml      # Flask + service + HPA
│   ├── database/statefulset.yaml    # PostgreSQL + PVC + secret
│   ├── network-policies/            # deny-all + allow rules
│   └── monitoring/                  # Prometheus + Grafana via Helm
└── .github/workflows/
    └── trivy-scan.yaml              # Security scanning CI pipeline
```
