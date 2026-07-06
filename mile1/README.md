# GitOps Platform (Beginner Friendly)

A simplified GitOps platform with:
- **ArgoCD** - Continuous deployment to Kubernetes
- **GitHub Actions** - CI pipeline (build, test, secrets scan)
- **Gitleaks** - Secrets scanning on every commit
- **Kustomize** - Environment configuration

## Quick Start

### Prerequisites
- Kubernetes cluster (local: kind, minikube, or Docker Desktop)
- kubectl configured
- GitHub account

### 1. Install ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
- URL: https://localhost:8080
- Username: `admin`
- Password: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d`

### 3. Deploy the App
```bash
kubectl apply -f argocd/application.yaml
```

### 4. Push to GitHub
1. Create a new repo on GitHub
2. Push this code:
```bash
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

### 5. Update ArgoCD Application
Edit `argocd/application.yaml` and change `repoURL` to your GitHub repo.

### 6. Watch It Deploy
ArgoCD will sync automatically. Check the UI or run:
```bash
kubectl get pods -n default
```

## Project Structure
```
.
├── .github/workflows/ci.yaml    # CI pipeline (build, test, gitleaks)
├── .gitleaks.toml               # Secrets scanning config
├── argocd/application.yaml      # ArgoCD app definition
├── apps/sample-app/
│   ├── src/main.go              # Simple Go web server
│   ├── Dockerfile               # Container build
│   └── k8s/base/
│       ├── deployment.yaml      # K8s deployment
│       ├── service.yaml         # K8s service
│       └── kustomization.yaml   # Kustomize base
└── README.md
```

## How It Works

1. **Push code** → GitHub Actions runs CI
2. **CI Pipeline** runs:
   - Gitleaks: Scans for secrets (API keys, tokens, passwords)
   - Build: Creates Docker image
   - Test: Runs tests inside container
3. **ArgoCD** watches the repo
4. **Auto-sync** deploys changes to Kubernetes

## Customize

### Change the App
Edit `apps/sample-app/src/main.go` and push.

### Change Image Registry
Edit `apps/sample-app/k8s/base/deployment.yaml`:
```yaml
image: ghcr.io/YOUR-USER/YOUR-REPO:latest
```

### Add Tests
Add tests in `apps/sample-app/src/` - CI will run them automatically.

## Common Commands

```bash
# Check ArgoCD app status
kubectl get applications -n argocd

# Force sync
argocd app sync sample-app

# View logs
kubectl logs -n default -l app=sample-app

# Port forward to test locally
kubectl port-forward -n default svc/sample-app 8080:8080
```

## Learn More
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)
- [Kustomize Docs](https://kustomize.io/)
- [Gitleaks Docs](https://github.com/gitleaks/gitleaks)
- [GitHub Actions Docs](https://docs.github.com/en/actions)