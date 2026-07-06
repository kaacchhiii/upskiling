#!/usr/bin/env bash
set -euo pipefail

# Install Prometheus + Grafana using Helm

echo "Adding Helm repo..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts 2>/dev/null || true
helm repo update

echo "Creating monitoring namespace..."
kubectl apply -f "$(dirname "$0")/namespace.yaml"

echo "Installing kube-prometheus-stack..."
helm upgrade --install kube-prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values "$(dirname "$0")/prometheus-values.yaml" \
  --wait \
  --timeout 10m

echo ""
echo "Done! Access Grafana:"
echo "  kubectl port-forward svc/kube-prometheus-grafana 3000:80 -n monitoring"
echo "  Open http://localhost:3000  (admin / admin)"
