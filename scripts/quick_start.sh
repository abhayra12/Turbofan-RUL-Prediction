#!/bin/bash
# Quick Start Script - Trains model and starts service

set -e

echo "=========================================="
echo "Turbofan RUL Prediction - Quick Start"
echo "=========================================="

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    else
        echo "Virtual environment not found. Please run ./scripts/setup.sh first"
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}[1/3] Training model...${NC}"
python train.py
echo -e "${GREEN}✓${NC} Model trained"

echo ""
echo -e "${YELLOW}[2/3] Starting prediction service...${NC}"
echo "Service will be available at http://localhost:8000"
echo "API documentation at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

# Start service
uvicorn predict:app --host 0.0.0.0 --port 8000 --reload
