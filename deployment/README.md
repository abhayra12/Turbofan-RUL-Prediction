# GCP Cloud Run Deployment

This directory contains deployment configuration and scripts for deploying the Turbofan RUL Prediction service to Google Cloud Run.

## Prerequisites

1. **GCP Account**: Active Google Cloud Platform account
2. **GCP Project**: A GCP project with billing enabled
3. **gcloud CLI**: Installed and configured ([Installation Guide](https://cloud.google.com/sdk/docs/install))
4. **Service Account**: GCP service account with required permissions
5. **Docker**: Installed locally (for local testing)

## Required GCP APIs

The deployment script will enable these APIs automatically:
- Cloud Build API
- Cloud Run API
- Container Registry API

## Service Account Permissions

Your service account needs the following roles:
- `roles/run.admin` - Cloud Run Admin
- `roles/iam.serviceAccountUser` - Service Account User
- `roles/cloudbuild.builds.editor` - Cloud Build Editor
- `roles/storage.admin` - Storage Admin (for Container Registry)

## Setup

### 1. Copy Service Account Credentials

Copy your GCP service account JSON file to the deployment directory:

```bash
cp /path/to/your/service-account-key.json deployment/gcp-credentials.json
```

**Note**: The credentials file is git-ignored for security.

### 2. Update Configuration (if needed)

Edit `deploy_gcp.sh` to customize:
```bash
PROJECT_ID="your-project-id"
SERVICE_NAME="turbofan-rul-prediction"
REGION="us-central1"
```

## Deployment

### Option 1: Using Deployment Script (Recommended)

```bash
cd deployment
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

The script will:
1. Authenticate with GCP
2. Set the project
3. Enable required APIs
4. Build Docker image
5. Push to Google Container Registry
6. Deploy to Cloud Run
7. Display the service URL

### Option 2: Manual Deployment

#### Step 1: Authenticate

```bash
gcloud auth activate-service-account --key-file=deployment/gcp-credentials.json
gcloud config set project upgrade-478511
```

#### Step 2: Build and Push Image

```bash
# Build the image
gcloud builds submit --tag gcr.io/upgrade-478511/turbofan-rul-prediction

# Or using Docker
docker build -t gcr.io/upgrade-478511/turbofan-rul-prediction .
docker push gcr.io/upgrade-478511/turbofan-rul-prediction
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy turbofan-rul-prediction \
  --image gcr.io/upgrade-478511/turbofan-rul-prediction \
  --platform managed \
  --region us-central1 \
  --port 8000 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --allow-unauthenticated
```

## Configuration

### Resource Allocation

Current configuration:
- **Memory**: 2 GiB (adequate for model inference)
- **CPU**: 2 vCPU (for faster predictions)
- **Timeout**: 300 seconds
- **Max Instances**: 10 (auto-scales based on traffic)
- **Min Instances**: 0 (scales to zero when idle)

Adjust in `deploy_gcp.sh` based on your needs.

### Environment Variables

Add environment variables in the deployment command:
```bash
--set-env-vars "ENVIRONMENT=production,LOG_LEVEL=INFO"
```

## Testing the Deployment

Once deployed, you'll receive a service URL like:
```
https://turbofan-rul-prediction-xxxxx-uc.a.run.app
```

### Test Health Check

```bash
curl https://your-service-url/health
```

### Test Prediction

```bash
curl -X POST https://your-service-url/predict \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": 1,
    "time_cycles": 100,
    "setting_1": 0.0023,
    "setting_2": 0.0003,
    "setting_3": 100.0,
    "sensor_1": 518.67,
    "sensor_2": 641.82,
    "sensor_3": 1589.70,
    "sensor_4": 1400.60,
    "sensor_5": 14.62,
    "sensor_6": 21.61,
    "sensor_7": 554.36,
    "sensor_8": 2388.06,
    "sensor_9": 9046.19,
    "sensor_10": 1.30,
    "sensor_11": 47.47,
    "sensor_12": 521.66,
    "sensor_13": 2388.02,
    "sensor_14": 8138.62,
    "sensor_15": 8.4195,
    "sensor_16": 0.03,
    "sensor_17": 392,
    "sensor_18": 2388,
    "sensor_19": 100.0,
    "sensor_20": 39.06,
    "sensor_21": 23.4190
  }'
```

### View API Documentation

Open in browser:
```
https://your-service-url/docs
```

## Monitoring

### View Logs

```bash
gcloud run services logs read turbofan-rul-prediction \
  --region us-central1 \
  --limit 100
```

### Service Details

```bash
gcloud run services describe turbofan-rul-prediction \
  --region us-central1
```

### Metrics

View metrics in [GCP Console](https://console.cloud.google.com/run):
- Request count
- Request latency
- Container CPU utilization
- Container memory utilization
- Billable container instance time

## Updating the Service

To update the service with new code:

```bash
cd deployment
./deploy_gcp.sh
```

Cloud Run will perform a rolling update with zero downtime.

## Rollback

To rollback to a previous revision:

```bash
# List revisions
gcloud run revisions list --service turbofan-rul-prediction --region us-central1

# Rollback to specific revision
gcloud run services update-traffic turbofan-rul-prediction \
  --to-revisions REVISION_NAME=100 \
  --region us-central1
```

## Cost Optimization

Cloud Run pricing is based on:
- **CPU and Memory**: Billed per 100ms of request processing
- **Requests**: $0.40 per million requests
- **Network Egress**: Standard rates

To minimize costs:
- Use `--min-instances 0` to scale to zero
- Right-size CPU and memory allocations
- Set appropriate request timeouts
- Use Cloud Run's free tier (2 million requests/month)

## Cleanup

To delete the service:

```bash
gcloud run services delete turbofan-rul-prediction \
  --region us-central1
```

To delete the container image:

```bash
gcloud container images delete gcr.io/upgrade-478511/turbofan-rul-prediction
```

## Troubleshooting

### Build Fails

- Check Dockerfile syntax
- Ensure all dependencies are in pyproject.toml
- Verify models directory is included

### Deployment Fails

- Check service account permissions
- Verify project billing is enabled
- Check quota limits

### Service Errors

- Check logs: `gcloud run services logs read`
- Verify model files are in the image
- Test locally first with Docker

### Connection Issues

- Verify service is deployed: `gcloud run services list`
- Check firewall rules
- Ensure service allows unauthenticated access (if intended)

## Security Best Practices

1. **Authentication**: Consider enabling Cloud Run authentication for production
2. **Secrets**: Use Secret Manager for sensitive data
3. **Network**: Use VPC connector for private resources
4. **Least Privilege**: Grant minimal required permissions
5. **Monitoring**: Enable Cloud Monitoring and Logging

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Best Practices](https://cloud.google.com/run/docs/best-practices)
- [Security Guide](https://cloud.google.com/run/docs/securing/overview)
