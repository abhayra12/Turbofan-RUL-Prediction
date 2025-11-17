#!/bin/bash
# Complete Setup Script for Turbofan RUL Prediction Project

set -e

echo "=========================================="
echo "Turbofan RUL Prediction - Setup"
echo "=========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -f "pyproject.toml" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}[1/5] Checking prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ Error: pip3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} pip3 found"

echo ""
echo -e "${YELLOW}[2/5] Installing UV package manager...${NC}"
if ! command -v uv &> /dev/null; then
    pip3 install uv
    echo -e "${GREEN}✓${NC} UV installed"
else
    echo -e "${GREEN}✓${NC} UV already installed"
fi

echo ""
echo -e "${YELLOW}[3/5] Creating virtual environment...${NC}"
if [ ! -d ".venv" ]; then
    uv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

echo ""
echo -e "${YELLOW}[4/5] Installing dependencies...${NC}"
source .venv/bin/activate
uv pip install -e .
echo -e "${GREEN}✓${NC} Dependencies installed"

echo ""
echo -e "${YELLOW}[5/5] Checking data...${NC}"
if [ ! -d "data/CMaps" ]; then
    echo -e "${YELLOW}⚠${NC} Dataset not found. Downloading..."
    mkdir -p data
    cd data
    curl -L -o nasa-cmaps.zip https://www.kaggle.com/api/v1/datasets/download/behrad3d/nasa-cmaps
    unzip -q nasa-cmaps.zip
    rm nasa-cmaps.zip
    cd ..
    echo -e "${GREEN}✓${NC} Dataset downloaded and extracted"
else
    echo -e "${GREEN}✓${NC} Dataset already present"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Train the model:"
echo "   python train.py"
echo ""
echo "3. Run prediction service:"
echo "   uvicorn predict:app --host 0.0.0.0 --port 8000"
echo ""
echo "4. Test the service:"
echo "   python test.py"
echo ""
echo "5. Or use the quick start script:"
echo "   ./scripts/quick_start.sh"
echo ""
echo "=========================================="
