#!/bin/bash
# GCP Cloud Run Deployment Script

set -e

# Configuration
PROJECT_ID="upgrade-478511"
SERVICE_NAME="turbofan-rul-prediction"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
PORT=8000

echo "=========================================="
echo "GCP Cloud Run Deployment"
echo "=========================================="
echo "Project ID: ${PROJECT_ID}"
echo "Service Name: ${SERVICE_NAME}"
echo "Region: ${REGION}"
echo "Image: ${IMAGE_NAME}"
echo "=========================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Authenticate using service account
echo ""
echo "[1/6] Authenticating with GCP..."
if [ -f "gcp-credentials.json" ]; then
    gcloud auth activate-service-account --key-file=gcp-credentials.json
    echo "✓ Authenticated using service account"
else
    echo "⚠ Warning: gcp-credentials.json not found in deployment directory"
    echo "Assuming already authenticated..."
fi

# Set project
echo ""
echo "[2/6] Setting GCP project..."
gcloud config set project ${PROJECT_ID}
echo "✓ Project set to ${PROJECT_ID}"

# Enable required APIs
echo ""
echo "[3/6] Enabling required GCP APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com
echo "✓ Required APIs enabled"

# Build Docker image
echo ""
echo "[4/6] Building Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} ..
echo "✓ Docker image built and pushed to GCR"

# Deploy to Cloud Run
echo ""
echo "[5/6] Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --port ${PORT} \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --allow-unauthenticated \
    --set-env-vars "ENVIRONMENT=production" \
    --quiet

echo "✓ Service deployed to Cloud Run"

# Get service URL
echo ""
echo "[6/6] Getting service URL..."
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo "=========================================="
echo "✅ DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo ""
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Test the service:"
echo "  Health check: curl ${SERVICE_URL}/health"
echo "  API docs: ${SERVICE_URL}/docs"
echo ""
echo "=========================================="
