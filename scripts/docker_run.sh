#!/bin/bash
# Docker Build and Run Script

set -e

echo "=========================================="
echo "Turbofan RUL Prediction - Docker"
echo "=========================================="

SERVICE_NAME="turbofan-rul-prediction"
IMAGE_NAME="turbofan-rul"
PORT=8000

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

echo ""
echo "[1/4] Building Docker image..."
docker build -t ${IMAGE_NAME}:latest .
echo "✓ Docker image built"

echo ""
echo "[2/4] Stopping existing container (if any)..."
docker stop ${SERVICE_NAME} 2>/dev/null || true
docker rm ${SERVICE_NAME} 2>/dev/null || true
echo "✓ Cleaned up existing container"

echo ""
echo "[3/4] Starting container..."
docker run -d \
    --name ${SERVICE_NAME} \
    -p ${PORT}:${PORT} \
    ${IMAGE_NAME}:latest

echo "✓ Container started"

echo ""
echo "[4/4] Waiting for service to be ready..."
sleep 5

# Check if service is running
if curl -s http://localhost:${PORT}/health > /dev/null; then
    echo "✓ Service is ready"
else
    echo "⚠ Service may still be starting..."
fi

echo ""
echo "=========================================="
echo "✅ Docker container is running!"
echo "=========================================="
echo ""
echo "Service URL: http://localhost:${PORT}"
echo "API Docs: http://localhost:${PORT}/docs"
echo "Health Check: http://localhost:${PORT}/health"
echo ""
echo "View logs:"
echo "  docker logs ${SERVICE_NAME}"
echo ""
echo "Stop container:"
echo "  docker stop ${SERVICE_NAME}"
echo ""
echo "Remove container:"
echo "  docker rm ${SERVICE_NAME}"
echo ""
echo "=========================================="
