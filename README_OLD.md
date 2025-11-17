# 🚀 Turbofan Engine Remaining Useful Life (RUL) Prediction

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ML Zoomcamp 2025 - Midterm Project**

A production-ready machine learning system for predicting the Remaining Useful Life (RUL) of turbofan engines using the NASA C-MAPSS dataset. This project implements a complete end-to-end ML pipeline from data ingestion to cloud deployment.

---

## 📋 Table of Contents

- [Problem Description](#-problem-description)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Model Performance](#-model-performance)
- [API Documentation](#-api-documentation)
- [Docker Deployment](#-docker-deployment)
- [Cloud Deployment](#-cloud-deployment)
- [Development](#-development)
- [Additional Documentation](#-additional-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Problem Description

### Business Context

Aircraft engine maintenance is critical for:
- **Safety**: Preventing catastrophic in-flight failures
- **Cost Efficiency**: Optimizing maintenance schedules and reducing unplanned downtime
- **Operational Continuity**: Ensuring flight reliability and reducing delays
- **Resource Optimization**: Better planning of spare parts and maintenance crews

Traditional reactive maintenance (fixing after failure) or time-based maintenance (fixed intervals) is inefficient. **Predictive maintenance** using machine learning can predict when an engine is likely to fail, enabling proactive maintenance.

### Problem Statement

Given sensor readings and operational settings from turbofan engines, **predict the Remaining Useful Life (RUL)** - the number of remaining operational cycles before the engine requires maintenance.

### Solution Approach

This project implements a supervised machine learning regression model that:
1. Ingests multi-variate time series sensor data from engines
2. Engineers relevant features including rolling statistics
3. Trains and compares multiple regression algorithms
4. Deploys the best model as a RESTful API service
5. Provides real-time RUL predictions for operational engines

### Use Cases

- **Airlines**: Schedule proactive maintenance before failure
- **Engine Manufacturers**: Improve engine design based on degradation patterns
- **Maintenance Crews**: Optimize resource allocation and spare parts inventory
- **Regulatory Compliance**: Ensure engines meet safety standards

---

## 📊 Dataset

### NASA C-MAPSS Dataset

The **Commercial Modular Aero-Propulsion System Simulation (C-MAPSS)** dataset from NASA Ames Prognostics Data Repository contains:

- **Source**: NASA Ames Research Center
- **Type**: Multivariate time series
- **Task**: Regression (predict RUL)
- **Sub-datasets**: 4 (FD001-FD004) with varying complexity
- **Engines**: 100-260 per dataset
- **Sensors**: 21 sensors + 3 operational settings

### Dataset Characteristics

| Sub-dataset | Train Engines | Test Engines | Operating Conditions | Fault Modes |
|------------|---------------|--------------|---------------------|-------------|
| FD001      | 100           | 100          | 1 (Sea Level)       | 1 (HPC)     |
| FD002      | 260           | 259          | 6                   | 1 (HPC)     |
| FD003      | 100           | 100          | 1 (Sea Level)       | 2 (HPC, Fan)|
| FD004      | 248           | 249          | 6                   | 2 (HPC, Fan)|

**This project uses FD001** for initial development (simplest scenario).

### Data Format

Each row represents a snapshot at a specific time cycle with:
- **Column 1**: Engine unit number
- **Column 2**: Time in cycles
- **Columns 3-5**: Operational settings (altitude, Mach number, etc.)
- **Columns 6-26**: Sensor measurements (temperatures, pressures, speeds, etc.)

### Download

The dataset is automatically downloaded during setup. Manual download:

```bash
curl -L -o nasa-cmaps.zip https://www.kaggle.com/api/v1/datasets/download/behrad3d/nasa-cmaps
unzip nasa-cmaps.zip -d data/
```

More details: [data/README.md](data/README.md)

---

## 📁 Project Structure

```
turbofan-rul-prediction/
│
├── data/                           # Dataset directory
│   ├── CMaps/                      # NASA C-MAPSS dataset files
│   └── README.md                   # Dataset documentation
│
├── models/                         # Saved model artifacts
│   ├── xgboost_rul_model.pkl      # Trained model
│   ├── scaler.pkl                 # Feature scaler
│   ├── config.pkl                 # Configuration
│   └── model_metadata.pkl         # Model metadata
│
├── deployment/                     # Deployment configurations
│   ├── deploy_gcp.sh              # GCP Cloud Run deployment script
│   ├── gcp-credentials.json       # GCP service account credentials (gitignored)
│   └── README.md                  # Deployment documentation
│
├── docs/                          # Documentation
│   └── ARCHITECTURE.md            # Architecture diagrams and explanations
│
├── scripts/                       # Automation scripts
│   ├── setup.sh                   # Complete project setup
│   ├── quick_start.sh             # Quick training and service start
│   └── docker_run.sh              # Docker build and run
│
├── notebook.ipynb                 # Jupyter notebook with EDA and experiments
├── train.py                       # Model training script
├── predict.py                     # FastAPI prediction service
├── test.py                        # Service testing script
│
├── pyproject.toml                 # Project dependencies (UV)
├── Dockerfile                     # Docker configuration
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🔧 Installation

### Prerequisites

- **Python**: 3.9 or higher (< 3.12)
- **pip**: Latest version
- **Docker**: For containerization (optional but recommended)
- **GCP Account**: For cloud deployment (optional)

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd turbofan-rul-prediction

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
1. Check prerequisites
2. Install UV package manager
3. Create virtual environment
4. Install all dependencies
5. Download the dataset

### Option 2: Manual Setup

```bash
# Install UV package manager
pip install uv

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e .

# Download dataset
mkdir -p data
cd data
curl -L -o nasa-cmaps.zip https://www.kaggle.com/api/v1/datasets/download/behrad3d/nasa-cmaps
unzip nasa-cmaps.zip
rm nasa-cmaps.zip
cd ..
```

---

## ⚡ Quick Start

### Option 1: One-Command Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Train model and start service
./scripts/quick_start.sh
```

### Option 2: Step-by-Step

```bash
# Activate virtual environment
source .venv/bin/activate

# 1. Train the model
python train.py

# 2. Start the prediction service
uvicorn predict:app --host 0.0.0.0 --port 8000

# 3. In another terminal, test the service
python test.py
```

### Option 3: Using Docker

```bash
# Build and run with Docker
./scripts/docker_run.sh

# Or manually
docker build -t turbofan-rul .
docker run -p 8000:8000 turbofan-rul
```

---

## 💻 Usage

### 1. Training the Model

```bash
python train.py
```

**Output:**
- Trained XGBoost model
- Feature scaler
- Configuration files
- Model metadata with performance metrics

**Training includes:**
- Data loading and preprocessing
- Feature engineering (rolling statistics)
- Training 5 different models
- Hyperparameter tuning
- Model evaluation and selection

### 2. Running the Prediction Service

```bash
uvicorn predict:app --host 0.0.0.0 --port 8000
```

**Access:**
- API Service: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Making Predictions

#### Using cURL

```bash
curl -X POST "http://localhost:8000/predict" \
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

#### Using Python

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "unit_id": 1,
    "time_cycles": 100,
    "setting_1": 0.0023,
    "setting_2": 0.0003,
    "setting_3": 100.0,
    # ... all sensor values ...
}

response = requests.post(url, json=data)
print(response.json())
# Output: {"unit_id": 1, "predicted_rul": 112.5, "confidence": "medium"}
```

#### Using Test Script

```bash
python test.py
```

---

## 📈 Model Performance

### Models Compared

1. **Linear Regression** - Baseline
2. **Ridge Regression** - L2 regularization
3. **Random Forest** - Ensemble tree-based
4. **Gradient Boosting** - Sequential ensemble
5. **XGBoost** - Optimized gradient boosting (✅ Selected)

### Final Model: XGBoost

**Best Hyperparameters** (from GridSearchCV):
```python
{
    'n_estimators': 200,
    'max_depth': 5,
    'learning_rate': 0.1,
    'subsample': 0.8
}
```

### Performance Metrics

**Test Set Results:**

| Metric | Value | Description |
|--------|-------|-------------|
| **RMSE** | ~18-22 cycles | Root Mean Squared Error |
| **MAE** | ~12-15 cycles | Mean Absolute Error |
| **R²** | ~0.75-0.85 | Coefficient of Determination |

**Interpretation:**
- On average, predictions are within 12-15 cycles of actual RUL
- Model explains 75-85% of variance in RUL
- Performance suitable for production predictive maintenance

### Feature Importance

Top features contributing to predictions:
1. Sensor readings (particularly sensors 4, 11, 15)
2. Rolling mean values (5-cycle window)
3. Rolling standard deviation (indicating degradation patterns)
4. Operational settings

---

## 📚 API Documentation

### Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "message": "Turbofan Engine RUL Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "predict": "/predict",
    "predict_batch": "/predict/batch",
    "model_info": "/model/info",
    "docs": "/docs"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "XGBoost",
  "test_rmse": 18.5432
}
```

#### `GET /model/info`
Get model metadata and performance.

**Response:**
```json
{
  "model_type": "XGBoost",
  "dataset": "FD001",
  "n_features": 25,
  "test_metrics": {
    "rmse": 18.5432,
    "mae": 13.2156,
    "r2": 0.8234
  },
  "training_date": "2025-11-17 10:30:45",
  "best_params": {
    "n_estimators": 200,
    "max_depth": 5,
    "learning_rate": 0.1,
    "subsample": 0.8
  }
}
```

#### `POST /predict`
Predict RUL for a single engine reading.

**Request Body:**
```json
{
  "unit_id": 1,
  "time_cycles": 100,
  "setting_1": 0.0023,
  "setting_2": 0.0003,
  "setting_3": 100.0,
  "sensor_1": 518.67,
  "sensor_2": 641.82,
  ...
  "sensor_21": 23.4190
}
```

**Response:**
```json
{
  "unit_id": 1,
  "predicted_rul": 112.5,
  "confidence": "medium"
}
```

**Confidence Levels:**
- `high`: RUL < 30 cycles (urgent maintenance needed)
- `medium`: RUL between 30-80 cycles (schedule maintenance soon)
- `low`: RUL > 80 cycles (engine in good condition)

#### `POST /predict/batch`
Predict RUL for multiple engine readings.

**Request Body:**
```json
{
  "readings": [
    { "unit_id": 1, "time_cycles": 100, ... },
    { "unit_id": 2, "time_cycles": 150, ... }
  ]
}
```

**Response:**
```json
{
  "predictions": [
    { "unit_id": 1, "predicted_rul": 112.5, "confidence": "medium" },
    { "unit_id": 2, "predicted_rul": 45.3, "confidence": "high" }
  ],
  "total_predictions": 2
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Build and Run

```bash
# Using the script
./scripts/docker_run.sh

# Or manually
docker build -t turbofan-rul .
docker run -d -p 8000:8000 --name turbofan-service turbofan-rul
```

### Docker Commands

```bash
# View logs
docker logs turbofan-service

# Stop container
docker stop turbofan-service

# Remove container
docker rm turbofan-service

# View running containers
docker ps
```

### Docker Image Details

- **Base Image**: python:3.11-slim
- **Size**: ~800 MB
- **Build Time**: ~3-5 minutes
- **Multi-stage**: Yes (builder + runtime)
- **Security**: Non-root user
- **Health Check**: Integrated

---

## ☁️ Cloud Deployment with GCP

### 🏗️ Google Cloud Build + ☁️ Cloud Run Deployment

This project leverages **Google Cloud Build** for automated containerization and **Google Cloud Run** for serverless deployment.

#### Architecture

```
GitHub Repository
      ↓
   🏗️ Cloud Build (builds Docker image)
      ↓
   🐳 Container Registry (stores image)
      ↓
   ☁️ Cloud Run (runs containerized service)
      ↓
   🌐 Live API endpoint
```

#### Prerequisites

1. GCP account with billing enabled
2. Service account with required permissions
3. gcloud CLI installed

#### Automated Deployment (Recommended)

```bash
cd deployment
./deploy_gcp.sh
```

**What this does:**
- 🏗️ Triggers Cloud Build to build Docker image from repository
- 📦 Pushes image to Google Container Registry
- ☁️ Deploys to Cloud Run with optimized settings
- ✅ Configures automatic health checks
- 🔄 Enables autoscaling

#### Manual Deployment

```bash
# Authenticate
gcloud auth activate-service-account --key-file=deployment/gcp-credentials.json
gcloud config set project upgrade-478511

# Option 1: Use Cloud Build (recommended for production)
gcloud builds submit --tag gcr.io/upgrade-478511/turbofan-rul-prediction

# Option 2: Direct deployment (development)
gcloud run deploy turbofan-rul-prediction \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --no-cpu-throttling \
  --concurrency 80
```

#### Post-Deployment Verification

**🎉 Live Service**: [https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app](https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app)

**📖 API Documentation**: [https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/docs](https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/docs)

**Test deployment:**
```bash
# ✅ Health check
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/health

# 📊 Model info
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/model/info

# 🔮 Make prediction
curl -X POST https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"unit_id":1,"time_cycles":100,"setting_1":0.0023,"setting_2":0.0003,"setting_3":100.0,"sensor_1":518.67,"sensor_2":641.82,"sensor_3":1589.70,"sensor_4":1400.60,"sensor_5":14.62,"sensor_6":21.61,"sensor_7":554.36,"sensor_8":2388.02,"sensor_9":9046.19,"sensor_10":1.30,"sensor_11":47.47,"sensor_12":521.66,"sensor_13":2388.02,"sensor_14":8138.62,"sensor_15":8.4195,"sensor_16":0.03,"sensor_17":392,"sensor_18":2388,"sensor_19":100.0,"sensor_20":39.06,"sensor_21":23.4190}'
```

#### Deployment Services

| Service | Purpose | Status |
|---------|---------|--------|
| 🏗️ **Cloud Build** | Automated Docker image building | ✅ Active |
| 🐳 **Container Registry** | Image storage | ✅ Active |
| ☁️ **Cloud Run** | Serverless container execution | ✅ Running |
| 📊 **Cloud Logging** | Centralized log management | ✅ Enabled |
| 📈 **Cloud Monitoring** | Metrics and performance tracking | ✅ Enabled |

#### Viewing in GCP Console

To view and manage your deployed service in **Google Cloud Console**:

**🔗 Direct Links:**
- **Cloud Run Services**: https://console.cloud.google.com/run?project=upgrade-478511
- **Cloud Build History**: https://console.cloud.google.com/cloud-build/builds?project=upgrade-478511
- **Cloud Logs**: https://console.cloud.google.com/logs?project=upgrade-478511
- **Container Registry**: https://console.cloud.google.com/gcr?project=upgrade-478511

**Manual Navigation:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: `upgrade-478511`
3. Navigate to **Cloud Run**
4. Click service: `turbofan-rul-prediction`

**Available in Console:**
- 📋 Service details and URL
- 📊 Revision history and traffic split
- 📈 Metrics (requests, latency, errors)
- 📝 Logs and debugging
- ⚙️ Configuration and environment variables
- 🔄 Autoscaling settings
- 🌐 Custom domain mapping

#### Deployment Screenshots

**🏗️ Cloud Build - Automated Docker Image Building:**

![Cloud Build Pipeline](screenshots/cloud-build.png)

**☁️ Cloud Run Service - Live Deployment:**

![Cloud Run Service](screenshots/cloud-run-service.png)

**Model Deployed on Google Cloud Run:**

![Model GCP Deployed](screenshots/model-gcp-deployed.png)

**API Service Test - Cloud Run:**

![API Cloud Run Service Test](screenshots/api-cloud-run-service-test.png)

---

## 🛠️ Development

### Project Setup for Development

```bash
# Clone repository
git clone <repository-url>
cd turbofan-rul-prediction

# Install with development dependencies
uv pip install -e ".[dev]"

# Run linters
black .
isort .
flake8 .

# Run tests
pytest tests/ -v
```

### Jupyter Notebook

The `notebook.ipynb` contains:
- Comprehensive EDA
- Feature engineering experiments
- Model comparison
- Visualization
- Performance analysis

```bash
# Start Jupyter
jupyter notebook notebook.ipynb
```

### Code Structure

- `train.py`: Model training pipeline
- `predict.py`: FastAPI service implementation
- `test.py`: Integration tests
- `notebook.ipynb`: Exploratory analysis

### Adding New Features

1. Update `train.py` with new feature engineering
2. Update `predict.py` to handle new features
3. Retrain model
4. Update tests
5. Update documentation

---

## 📖 Additional Documentation

- [Data Documentation](data/README.md) - Dataset details and structure
- [Architecture](docs/ARCHITECTURE.md) - System architecture and diagrams
- [Deployment Guide](deployment/README.md) - Cloud deployment instructions

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **DataTalks.Club** - ML Zoomcamp 2025
- **NASA** - C-MAPSS Dataset
- **Kaggle** - Dataset hosting
- **A. Saxena et al.** - Original research paper

---

## 📧 Contact

**Author**: Abhay Ahirkar  
**Email**: abhayahirkar2@gmail.com  
**GitHub**: [@abhayra12](https://github.com/abhayra12)  
**Project**: ML Zoomcamp 2025 Midterm Project  
**Course**: [Machine Learning Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp)

---

## 🌟 Star the Repository

If you find this project useful, please consider giving it a ⭐!

---

**Built with ❤️ for ML Zoomcamp 2025**
