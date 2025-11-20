# Turbofan Engine RUL Prediction - Project Presentation

**Presenter:** Abhay Ahirkar  
**Date:** November 2025  
**Context:** ML Zoomcamp 2025 Midterm Project

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement & Business Impact](#problem-statement--business-impact)
3. [Tech Stack & Tools](#tech-stack--tools)
4. [Architecture & Design](#architecture--design)
5. [Development Journey](#development-journey)
6. [Model Selection & Results](#model-selection--results)
7. [Containerization & Deployment](#containerization--deployment)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [Challenges & Solutions](#challenges--solutions)
10. [Key Learnings](#key-learnings)
11. [Demo & Links](#demo--links)

---

## Project Overview

### What is this project?

A **production-ready ML system** that predicts the Remaining Useful Life (RUL) of turbofan aircraft engines using sensor data, enabling proactive maintenance scheduling.

### Key Deliverables

- ✅ End-to-end ML pipeline (EDA → Training → Deployment)
- ✅ REST API with 7 endpoints (FastAPI)
- ✅ Docker containerization (multi-stage build)
- ✅ Cloud deployment on Google Cloud Run
- ✅ Automated CI/CD with Cloud Build
- ✅ Full reproducibility (scripts, dependencies, documentation)

---

## Problem Statement & Business Impact

### The Challenge

Traditional aircraft maintenance follows two flawed approaches:

| Approach | Problem |
|----------|---------|
| **Reactive** | Fix after failure → Safety risks, unpredictable downtime |
| **Time-based** | Fixed service intervals → Unnecessary maintenance, wasted resources |

### The Solution

**Predictive Maintenance** using ML to forecast when engines will need service based on actual degradation patterns.

### Business Value

- 🛡️ **Safety**: Prevent catastrophic failures
- 💰 **Cost**: Reduce unnecessary maintenance + eliminate emergency repairs
- 📅 **Planning**: Optimize spare parts inventory and crew scheduling
- ✈️ **Uptime**: Minimize flight delays and maximize asset utilization

### Technical Problem

- **Input**: 21 sensor measurements + 3 operational settings per engine cycle
- **Output**: Predicted RUL (Remaining Useful Life) in cycles
- **Approach**: Supervised regression with time series features
- **Dataset**: NASA C-MAPSS (100 engines training, 100 engines test)

---

## Tech Stack & Tools

### Core ML & Data Tools

| Tool | Purpose | Why I Chose It |
|------|---------|----------------|
| **Python 3.11** | Core language | Industry standard, rich ML ecosystem |
| **NumPy 2.3.5** | Numerical computing | Fast array operations, sensor data processing |
| **pandas 2.3.3** | Data manipulation | Time series handling, feature engineering |
| **scikit-learn 1.7.2** | Preprocessing & evaluation | StandardScaler, train/test split, metrics |
| **XGBoost 3.1.1** | Production model | Best performance, fast inference, robust |
| **matplotlib + seaborn** | Visualization | EDA, correlation analysis, degradation plots |

### API & Web Framework

| Tool | Purpose | Why I Chose It |
|------|---------|----------------|
| **FastAPI 0.121.2** | REST API framework | Modern, async, auto-documentation, type validation |
| **Uvicorn 0.38.0** | ASGI server | High-performance async server for FastAPI |
| **Pydantic** | Data validation | Type-safe request/response models |

### Containerization & Deployment

| Tool | Purpose | Why I Chose It |
|------|---------|----------------|
| **Docker** | Containerization | Reproducibility, portability, isolation |
| **Google Cloud Build** | CI/CD automation | Seamless integration with GCP, automated builds |
| **Google Cloud Run** | Serverless deployment | Auto-scaling, pay-per-use, zero infrastructure management |
| **Google Container Registry** | Image storage | Native GCP integration, secure private registry |

### Development & Package Management

| Tool | Purpose | Why I Chose It |
|------|---------|----------------|
| **UV** | Package manager | Fast, modern alternative to pip |
| **pyproject.toml** | Dependency management | Modern Python standard, reproducible environments |
| **Jupyter** | EDA & experimentation | Interactive analysis, visualizations |
| **Git + GitHub** | Version control | Collaboration, CI/CD integration |

---

## Architecture & Design

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DEVELOPMENT                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   EDA        │──────▶│  Feature     │──────▶│   Model      │  │
│  │ (notebook)   │      │ Engineering  │      │  Training    │  │
│  │              │      │ (train.py)   │      │ (train.py)   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│         │                      │                      │          │
│         │                      │                      ▼          │
│         │                      │             ┌──────────────┐   │
│         │                      │             │   models/    │   │
│         │                      │             │ *.pkl files  │   │
│         │                      │             └──────────────┘   │
│         │                      │                      │          │
│         ▼                      ▼                      ▼          │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              NASA C-MAPSS Dataset                       │    │
│  │  (21 sensors × N cycles × 100 engines)                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ git push
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CI/CD PIPELINE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │   GitHub     │──────▶│ Cloud Build  │──────▶│  Container   │  │
│  │  Repository  │      │ (automated)  │      │   Registry   │  │
│  │              │      │              │      │ (gcr.io)     │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                                │                      │          │
│                                │                      │          │
│                                ▼                      ▼          │
│                       ┌──────────────┐      ┌──────────────┐   │
│                       │ Dockerfile   │      │ Docker Image │   │
│                       │ (multi-stage)│      │ (~800 MB)    │   │
│                       └──────────────┘      └──────────────┘   │
│                                                       │          │
└───────────────────────────────────────────────────────┼─────────┘
                                                        │
                                                        │ deploy
                                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PRODUCTION                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌──────────────────────┐                      │
│                    │   Google Cloud Run   │                      │
│                    │   (Serverless)       │                      │
│                    └──────────────────────┘                      │
│                              │                                    │
│                              │                                    │
│              ┌───────────────┼───────────────┐                   │
│              │               │               │                   │
│              ▼               ▼               ▼                   │
│      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│      │  Container  │ │  Container  │ │  Container  │           │
│      │  Instance 1 │ │  Instance 2 │ │  Instance N │           │
│      │             │ │             │ │ (auto-scale)│           │
│      └─────────────┘ └─────────────┘ └─────────────┘           │
│              │               │               │                   │
│              └───────────────┼───────────────┘                   │
│                              │                                    │
│                              ▼                                    │
│                    ┌──────────────────────┐                      │
│                    │   FastAPI Endpoints  │                      │
│                    ├──────────────────────┤                      │
│                    │ GET  /               │                      │
│                    │ GET  /health         │                      │
│                    │ GET  /model/info     │                      │
│                    │ POST /predict        │                      │
│                    │ POST /predict/batch  │                      │
│                    │ GET  /ping           │                      │
│                    │ GET  /docs           │                      │
│                    └──────────────────────┘                      │
│                              │                                    │
│                              ▼                                    │
│                    ┌──────────────────────┐                      │
│                    │   External Users     │                      │
│                    │   (API Clients)      │                      │
│                    └──────────────────────┘                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
Input Data (JSON)
    │
    ▼
┌─────────────────┐
│ FastAPI Router  │  ← Request validation (Pydantic)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Data Processing │  ← Feature engineering (rolling stats)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Feature Scaling │  ← StandardScaler (loaded from models/)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ XGBoost Model   │  ← Prediction (loaded from models/)
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Response Format │  ← JSON response with RUL + confidence
└─────────────────┘
    │
    ▼
Output (JSON)
```

### Project Structure

```
turbofan-rul-prediction/
│
├── 📊 notebook.ipynb          # EDA, visualization, experimentation
├── 🐍 train.py                # Model training pipeline
├── 🌐 predict.py              # FastAPI service
├── 🧪 test.py                 # Integration tests
│
├── 📁 models/                 # Trained artifacts
│   ├── xgboost_rul_model.pkl
│   ├── scaler.pkl
│   ├── feature_names.pkl
│   ├── config.pkl
│   └── model_metadata.pkl
│
├── 📁 data/                   # Dataset
│   └── CMaps/
│       ├── train_FD001.txt
│       ├── test_FD001.txt
│       └── RUL_FD001.txt
│
├── 📁 deployment/             # Cloud deployment
│   ├── deploy_gcp.sh
│   └── README.md
│
├── 📁 screenshots/            # Documentation
│   ├── cloud-build.png
│   ├── cloud-run-service.png
│   └── ...
│
├── 🐳 Dockerfile              # Multi-stage build
├── 📄 pyproject.toml          # Dependencies
└── 📝 README.md               # Documentation
```

---

## Development Journey

### Phase 1: Problem Understanding & EDA

**Duration:** ~2 days  
**Goal:** Understand the data and identify patterns

#### Steps I Took:

1. **Dataset Exploration**
   - Downloaded NASA C-MAPSS dataset (4 sub-datasets, used FD001)
   - 100 training engines, 100 test engines
   - 21 sensors + 3 operational settings per cycle
   - No missing values ✅

2. **Exploratory Data Analysis**
   - Time series plots for each engine's sensor readings
   - Correlation matrix to identify redundant sensors
   - RUL distribution analysis
   - Sensor degradation pattern visualization

3. **Key Findings**
   - Sensors 4, 11, 15 showed strongest correlation with degradation
   - Clear non-linear degradation patterns
   - Operational settings (altitude, Mach, throttle) influence sensor readings
   - Some sensors were constant (removed during feature engineering)

**Tools Used:** Jupyter, pandas, matplotlib, seaborn

---

### Phase 2: Feature Engineering

**Duration:** ~1 day  
**Goal:** Create meaningful features that capture degradation

#### Approach:

**Original Features (24):**
- 3 operational settings
- 21 sensor measurements

**Engineered Features (21 additional):**
- **Rolling Mean (7 features)**: 5-cycle moving average for key sensor groups
- **Rolling Std Dev (7 features)**: 5-cycle standard deviation (volatility)

**Why Rolling Statistics?**
- Raw sensors are noisy
- Degradation is a trend, not a single reading
- Rolling stats smooth out noise and capture patterns

**Total Features:** 45

**Feature Scaling:**
- Applied `StandardScaler` (mean=0, std=1)
- Critical for tree-based models and neural networks

**Implementation:**
```python
# Simplified version from train.py
def add_features(df):
    # Rolling mean
    df['rolling_mean'] = df.groupby('unit_id')['sensor_4'].rolling(5).mean()
    
    # Rolling std
    df['rolling_std'] = df.groupby('unit_id')['sensor_4'].rolling(5).std()
    
    return df
```

---

### Phase 3: Model Selection & Training

**Duration:** ~2 days  
**Goal:** Find the best model for production

#### Models I Evaluated:

| Model | Type | Training Time | Test RMSE | R² Score | Pros | Cons |
|-------|------|---------------|-----------|----------|------|------|
| **Linear Regression** | Baseline | ~1 sec | 28.34 | 0.62 | Fast, interpretable | Poor performance |
| **Ridge Regression** | Regularized | ~1 sec | 28.12 | 0.63 | Slight improvement | Still underfitting |
| **Random Forest** | Ensemble | ~45 sec | 22.45 | 0.76 | Good performance | Larger model size |
| **Gradient Boosting** | Ensemble | ~60 sec | 21.12 | 0.79 | Strong performance | Slower training |
| **XGBoost** ⭐ | Optimized Boosting | ~30 sec | **18.54** | **0.82** | **Best balance** | Requires tuning |

#### Why I Chose XGBoost:

1. **Best Performance**: Lowest RMSE (18.54), highest R² (0.82)
2. **Production-Friendly**: Fast inference (~10ms per prediction)
3. **Model Size**: ~5 MB (manageable in Docker)
4. **Robustness**: Handles non-linear patterns well
5. **Industry Standard**: Proven in production systems

#### Hyperparameter Tuning:

Used `GridSearchCV` with 5-fold cross-validation:

```python
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}
```

**Optimal Parameters:**
```python
{
    'n_estimators': 200,
    'max_depth': 5,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8
}
```

#### Final Results:

```
Test Set Metrics:
- RMSE: 18.54 cycles
- MAE:  13.22 cycles
- R²:   0.82

Interpretation:
- Model predictions are ±18 cycles off on average
- Explains 82% of variance in engine degradation
- Suitable for production predictive maintenance
```

**Training Script:**
```bash
python train.py
# Output: Saves 5 artifacts to models/
```

---

### Phase 4: API Development

**Duration:** ~1.5 days  
**Goal:** Create a production-ready REST API

#### Design Decisions:

**Framework Choice: FastAPI**
- Modern, async Python framework
- Auto-generated OpenAPI docs
- Type validation with Pydantic
- High performance (async I/O)

#### API Endpoints (7 total):

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/` | GET | API info | <5 ms |
| `/health` | GET | Health check | <10 ms |
| `/model/info` | GET | Model metadata | <10 ms |
| `/predict` | POST | Single prediction | ~15 ms |
| `/predict/batch` | POST | Batch predictions | ~50 ms |
| `/ping` | GET | Connectivity test | <5 ms |
| `/docs` | GET | Interactive docs | N/A |

#### Key Features:

1. **Type Safety**
   ```python
   class PredictionRequest(BaseModel):
       unit_id: int
       time_cycles: int
       setting_1: float
       # ... 21 sensors
   ```

2. **Error Handling**
   ```python
   try:
       prediction = model.predict(features)
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))
   ```

3. **Health Checks**
   ```python
   @app.get("/health")
   def health():
       return {
           "status": "healthy",
           "model_loaded": model is not None,
           "test_rmse": 18.54
       }
   ```

4. **Auto-Documentation**
   - Visit `/docs` for interactive Swagger UI
   - Try endpoints directly in browser

**Local Testing:**
```bash
# Start server
uvicorn predict:app --port 8000

# Test
curl http://localhost:8000/health
```

---

### Phase 5: Containerization

**Duration:** ~1 day  
**Goal:** Create a reproducible Docker image

#### Docker Strategy: Multi-Stage Build

**Why Multi-Stage?**
- Separate build dependencies from runtime
- Smaller final image (~800 MB vs 1.5 GB)
- Faster startup time
- Better security (no build tools in production)

#### Dockerfile Structure:

```dockerfile
# ================== Stage 1: Builder ==================
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY pyproject.toml .

# Create virtual environment
RUN pip install uv && uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN uv pip install -e .

# ================== Stage 2: Runtime ==================
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY predict.py .
COPY models/ models/

# Expose port
ENV PORT=8000
EXPOSE 8000

# Run server
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Key Optimizations:

1. **Layer Caching**: Dependencies installed before code copy
2. **Minimal Base**: `python:3.11-slim` (not full python image)
3. **Cleanup**: Removed apt cache to reduce size
4. **Virtual Environment**: Isolated dependencies

**Build & Test Locally:**
```bash
# Build
docker build -t turbofan-rul:latest .

# Run
docker run -p 8000:8000 turbofan-rul:latest

# Test
curl http://localhost:8000/health
```

---

### Phase 6: Cloud Deployment

**Duration:** ~2 days  
**Goal:** Deploy to production with automated CI/CD

#### Cloud Platform: Google Cloud Run

**Why Cloud Run?**
- ✅ Serverless (no infrastructure management)
- ✅ Auto-scaling (0 to N instances)
- ✅ Pay-per-use (cost-effective)
- ✅ Native Docker support
- ✅ HTTPS by default
- ✅ Built-in load balancing

#### Deployment Architecture:

```
GitHub Repository
    │
    │ (1) git push
    ▼
Cloud Build (Triggered)
    │
    │ (2) reads cloudbuild.yaml
    ▼
Docker Build
    │
    │ (3) builds image
    ▼
Container Registry (gcr.io)
    │
    │ (4) stores image
    ▼
Cloud Run (Deploy)
    │
    │ (5) pulls image
    ▼
Live Service (HTTPS URL)
```

#### Deployment Script (`deployment/deploy_gcp.sh`):

```bash
#!/bin/bash
set -e

PROJECT_ID="upgrade-478511"
SERVICE_NAME="turbofan-rul-prediction"
REGION="us-central1"

echo "🏗️  Submitting build to Cloud Build..."
gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --project=$PROJECT_ID

echo "☁️  Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --project $PROJECT_ID

echo "✅ Deployment complete!"
gcloud run services describe $SERVICE_NAME --region $REGION --project $PROJECT_ID
```

#### Configuration:

- **Memory**: 2 GB (model loading + inference)
- **CPU**: 2 vCPU (parallel request handling)
- **Max Instances**: 10 (cost control)
- **Concurrency**: 80 requests per instance
- **Timeout**: 300 seconds

#### Live Service:

- **URL**: https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app
- **Status**: ✅ Running
- **Region**: us-central1
- **Auto-scaling**: Active

**Testing Deployment:**
```bash
# Health check
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/health

# Model info
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/model/info

# Prediction (example)
curl -X POST "https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"unit_id": 1, "time_cycles": 100, ...}'
```

---

## CI/CD Pipeline

### Automated Build & Deploy Workflow

#### Trigger: Git Push to Main

```bash
git push origin main
```

#### Cloud Build Process:

1. **Detect Changes**
   - Cloud Build watches GitHub repository
   - Triggered on push to `main` branch

2. **Build Docker Image**
   - Reads `Dockerfile` from repo
   - Executes multi-stage build
   - Tags image with commit SHA

3. **Push to Registry**
   - Uploads image to Google Container Registry
   - Stores at `gcr.io/upgrade-478511/turbofan-rul-prediction`

4. **Deploy to Cloud Run**
   - Pulls latest image from registry
   - Updates Cloud Run service
   - Zero-downtime deployment (gradual rollout)

5. **Health Check**
   - Cloud Run pings `/health` endpoint
   - Service becomes live only if healthy

#### Build Configuration (`cloudbuild.yaml`):

```yaml
steps:
  # Step 1: Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/turbofan-rul-prediction'
      - '.'

  # Step 2: Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/turbofan-rul-prediction'

  # Step 3: Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'turbofan-rul-prediction'
      - '--image=gcr.io/$PROJECT_ID/turbofan-rul-prediction'
      - '--region=us-central1'
      - '--platform=managed'

images:
  - 'gcr.io/$PROJECT_ID/turbofan-rul-prediction'

timeout: 1200s
```

#### Build Logs & Monitoring:

- **Cloud Build History**: https://console.cloud.google.com/cloud-build/builds?project=upgrade-478511
- **Cloud Run Logs**: https://console.cloud.google.com/logs?project=upgrade-478511
- **Metrics**: Requests/sec, latency, error rate

#### Benefits of CI/CD:

✅ **Automation**: No manual deployment steps  
✅ **Consistency**: Same build process every time  
✅ **Rollback**: Easy to revert to previous version  
✅ **Visibility**: Build logs and deployment history  
✅ **Speed**: ~5 minutes from push to production

---

## Challenges & Solutions

### Challenge 1: Cloud Build Failure - Missing Models

**Problem:**
```
ERROR: COPY failed: file not found in build context or excluded by .dockerignore
COPY models/ models/
```

**Root Cause:**
- `.gitignore` excluded `*.pkl` files
- Model artifacts were not committed to GitHub
- Cloud Build couldn't find `models/` directory in build context

**Investigation Steps:**
1. Checked local directory: `models/` existed locally ✅
2. Checked GitHub repo: `models/` was empty ❌
3. Checked `.gitignore`: Found `*.pkl` exclusion rule

**Solution:**
1. Edited `.gitignore` to allow model files:
   ```diff
   - *.pkl
   + # *.pkl  (commented out)
   ```

2. Committed model artifacts:
   ```bash
   git add models/*.pkl
   git commit -m "fix: add model artifacts for Cloud Build"
   git push origin main
   ```

3. Re-triggered Cloud Build → Success ✅

**Key Learning:**
- Docker build context includes only committed files
- Large models need careful `.gitignore` management
- Alternative: Download models from cloud storage during build

---

### Challenge 2: Balancing Model Complexity vs. Deployment

**Problem:**
- Initial model: Stacked ensemble (Random Forest + XGBoost + Neural Network)
- Model size: ~150 MB
- Docker image: ~2.5 GB
- Inference time: ~200 ms per prediction
- Cold start: ~30 seconds

**Why This Was a Problem:**
- Cloud Run limits: 2 GB memory recommended
- Slow cold starts impact user experience
- Higher costs due to longer compute time

**Analysis:**
| Model | RMSE | Size | Inference Time | Complexity |
|-------|------|------|----------------|------------|
| Ensemble | 17.8 | 150 MB | 200 ms | Very High |
| XGBoost Only | 18.5 | 5 MB | 15 ms | Medium |
| Random Forest | 22.4 | 80 MB | 50 ms | High |

**Solution:**
- **Chose XGBoost standalone**
- Sacrificed 0.7 RMSE (17.8 → 18.5) for:
  - 30× smaller model (150 MB → 5 MB)
  - 13× faster inference (200 ms → 15 ms)
  - 3× smaller Docker image (2.5 GB → 800 MB)
  - <5 second cold start

**Key Learning:**
- Production ML is about trade-offs, not just accuracy
- "Good enough" and fast beats "perfect" and slow
- Always consider deployment constraints early

---

### Challenge 3: Feature Engineering Reproducibility

**Problem:**
- Training script generated features one way
- Prediction API generated features differently
- Results: Inference errors and wrong predictions

**Example:**
```python
# Training (train.py) - WRONG
df['rolling_mean'] = df['sensor_4'].rolling(5).mean()

# Prediction (predict.py) - WRONG
df['rolling_mean'] = df['sensor_4'].rolling(3).mean()  # Different window!
```

**Solution:**
1. **Centralized Feature Engineering**:
   - Extracted feature engineering to shared function
   - Saved feature engineering config as `config.pkl`

2. **Saved Feature Metadata**:
   ```python
   # During training
   feature_config = {
       'rolling_window': 5,
       'feature_names': [...],
       'scaler_params': {...}
   }
   pickle.dump(feature_config, 'models/config.pkl')
   ```

3. **Loaded Config During Inference**:
   ```python
   # During prediction
   config = pickle.load('models/config.pkl')
   df['rolling_mean'] = df['sensor_4'].rolling(config['rolling_window']).mean()
   ```

**Key Learning:**
- Feature engineering must be identical in training and inference
- Save all preprocessing parameters as artifacts
- Test training → inference pipeline end-to-end

---

### Challenge 4: Dependency Management Chaos

**Problem:**
- Different environments (local, Docker, Cloud Run) had different package versions
- `pip install` was slow (~5 minutes in Docker build)
- Reproducibility issues (works on my machine, fails in cloud)

**Solution:**
1. **Switched to UV Package Manager**:
   - 10-100× faster than pip
   - Better dependency resolution
   - Lock file for reproducibility

2. **Pinned Exact Versions**:
   ```toml
   [project.dependencies]
   python = "^3.11"
   pandas = "2.3.3"
   xgboost = "3.1.1"
   fastapi = "0.121.2"
   # ... exact versions
   ```

3. **Validated Environments**:
   ```bash
   # Local
   uv pip list > local_deps.txt
   
   # Docker
   docker run turbofan-rul pip list > docker_deps.txt
   
   # Compare
   diff local_deps.txt docker_deps.txt
   ```

**Key Learning:**
- Always pin exact versions in production
- Use lock files for reproducibility
- Modern tools (UV) can drastically speed up builds

---

### Challenge 5: Documentation vs. Implementation Drift

**Problem:**
- README instructions didn't match actual code
- Screenshots showed old service URL
- Documentation outdated after refactoring

**Solution:**
1. **Single Source of Truth**:
   - Updated README after every significant change
   - Stored config in code (not just docs)

2. **Automated Verification**:
   - Added `test.py` to validate API responses
   - Ran tests before updating docs

3. **Screenshot Management**:
   - Stored screenshots in `screenshots/` directory
   - Referenced with relative paths in README
   - Committed screenshots to Git

**Key Learning:**
- Documentation is code — version control it
- Test your own documentation (run the commands)
- Automate verification where possible

---

## Key Learnings

### Technical Learnings

1. **Production ML ≠ Research ML**
   - Accuracy isn't everything — latency, size, cost matter
   - "Deployable and maintainable" beats "state-of-the-art"

2. **Feature Engineering is Critical**
   - Rolling statistics captured degradation better than raw sensors
   - Domain knowledge (aviation, sensors) improved features significantly

3. **Containerization is Essential**
   - Docker ensures reproducibility across environments
   - Multi-stage builds reduce image size by 50%+

4. **CI/CD Saves Time**
   - Automated deployment reduces errors
   - 5-minute deploys vs. 30-minute manual process

5. **Cloud Run is Ideal for ML APIs**
   - Serverless simplifies ops (no Kubernetes complexity)
   - Auto-scaling handles variable load
   - Pay-per-use is cost-effective for low-traffic projects

### Process Learnings

1. **Start Simple, Then Optimize**
   - Built basic API first, then added batch prediction
   - Deployed single model first, then considered ensembles

2. **Document as You Go**
   - Writing README forced me to clarify design decisions
   - Screenshots captured progress (useful for debugging)

3. **Test in Production-Like Environment Early**
   - Local testing doesn't catch all deployment issues
   - Deploy to cloud early and iterate

4. **Git is Your Friend**
   - Commit frequently with clear messages
   - Easy to rollback when experiments fail

### Soft Skills

1. **Problem-Solving**
   - Cloud Build failure taught me to debug methodically
   - Checked logs, local files, Git history systematically

2. **Trade-Off Analysis**
   - Model complexity vs. deployment constraints
   - Accuracy vs. latency vs. cost

3. **Communication**
   - Documented architecture for future maintainers
   - Clear README helps others reproduce the work

---

## Demo & Links

### Live Service

- **API URL**: https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app
- **Interactive Docs**: https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/docs

### Quick Demo Commands

```bash
# 1. Health Check
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/health

# 2. Model Info
curl https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/model/info

# 3. Single Prediction (example data)
curl -X POST "https://turbofan-rul-prediction-4zi32kcrrq-uc.a.run.app/predict" \
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
    "sensor_8": 2388.02,
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

### Repository

- **GitHub**: https://github.com/abhayra12/Turbofan-RUL-Prediction
- **README**: Comprehensive documentation with screenshots
- **Reproducibility**: All scripts and dependencies included

### GCP Console

- **Cloud Run**: https://console.cloud.google.com/run?project=upgrade-478511
- **Cloud Build**: https://console.cloud.google.com/cloud-build/builds?project=upgrade-478511
- **Logs**: https://console.cloud.google.com/logs?project=upgrade-478511

---

## Anticipated Follow-Up Questions

### Q1: "What was the hardest technical challenge?"

**Answer:**
Balancing model performance with deployment constraints. Initially, I built a complex ensemble model (Random Forest + XGBoost + Neural Network) that achieved RMSE of 17.8 — slightly better than XGBoost alone (18.5). But the ensemble was:
- 30× larger (150 MB vs 5 MB)
- 13× slower (200 ms vs 15 ms inference)
- Required 3× more Docker image space

I had to make the tough decision to sacrifice 0.7 RMSE for massive gains in speed, size, and maintainability. This taught me that production ML is about trade-offs, not just leaderboard scores.

---

### Q2: "How did you ensure reproducibility?"

**Answer:**
Five key steps:

1. **Pinned Dependencies**: Used `pyproject.toml` with exact versions (`xgboost==3.1.1` not `xgboost>=3`)
2. **Saved All Artifacts**: Committed model `.pkl` files, scaler, feature names, config to Git
3. **Docker**: Containerized entire environment — works identically everywhere
4. **Scripts**: Automated setup (`scripts/setup.sh`), training (`train.py`), deployment (`deployment/deploy_gcp.sh`)
5. **Documentation**: Step-by-step README with exact commands

Anyone can clone the repo and reproduce results in ~10 minutes.

---

### Q3: "Why Cloud Run instead of Kubernetes or EC2?"

**Answer:**
Three reasons:

1. **Simplicity**: No cluster management, no node scaling, no YAML hell
2. **Cost**: Pay-per-request (serverless) vs. paying for idle VMs
3. **Auto-scaling**: Handles 1 request/day or 10,000 requests/hour automatically

For a single model API with variable traffic, Cloud Run is ideal. If I needed GPU inference or multi-model serving, I'd consider Vertex AI or GKE.

---

### Q4: "What would you do differently if you started over?"

**Answer:**
Three things:

1. **Think Deployment First**: I spent 2 days building a complex ensemble before realizing it wouldn't fit in Cloud Run's memory. Should have tested deployment constraints earlier.

2. **More Automated Testing**: I wrote `test.py` late in the project. Should have added integration tests from day 1 to catch feature engineering bugs earlier.

3. **Consider Model Registry**: For production, I'd use a model registry (MLflow, Vertex AI) instead of committing `.pkl` files to Git. Easier versioning and rollback.

---

### Q5: "How does this compare to your previous projects?"

**Answer:**
This is my first **end-to-end** ML project with:
- Production deployment (not just notebooks)
- CI/CD automation (not manual steps)
- Cloud infrastructure (not just localhost)
- Full reproducibility (not "works on my machine")

Previous projects were more focused on model accuracy. This one taught me **MLOps** — the engineering side of ML. I'm now comfortable with Docker, cloud deployment, and production best practices.

---

### Q6: "What's next for this project?"

**Answer:**
If I were to extend this, I'd add:

1. **Monitoring & Alerting**
   - Track prediction latency, error rates
   - Set up alerts if service degrades

2. **Model Versioning**
   - Deploy multiple model versions (A/B testing)
   - Gradual rollout of new models

3. **Data Drift Detection**
   - Monitor input data distribution
   - Retrain if sensor patterns change

4. **GPU Acceleration**
   - For larger models or batch inference
   - Cloud Run GPU support or Vertex AI

5. **Frontend Dashboard**
   - Visualize predictions over time
   - Interactive RUL charts per engine

---

## Summary

### What I Built

- ✅ End-to-end ML pipeline (EDA → Training → API → Deployment)
- ✅ XGBoost model with 82% R² score (18.54 RMSE)
- ✅ FastAPI REST service with 7 endpoints
- ✅ Multi-stage Docker container (~800 MB)
- ✅ Automated CI/CD with Google Cloud Build
- ✅ Production deployment on Cloud Run (live, auto-scaling)
- ✅ Fully reproducible with scripts and docs

### What I Learned

- Production ML requires balancing accuracy, speed, cost, and maintainability
- Feature engineering (rolling stats) was more impactful than complex models
- Docker + CI/CD make deployment reliable and repeatable
- Cloud Run is ideal for ML APIs (serverless, auto-scaling, cost-effective)
- Documentation and reproducibility are as important as code quality

### What I'm Proud Of

- Complete end-to-end system (not just a model)
- Production-grade code (error handling, logging, health checks)
- Solved real deployment challenges (Cloud Build failure, dependency hell)
- Clean, documented, reproducible codebase
- Live service that anyone can use

---

**Thank you for your time!**

Questions? Let's discuss! 🚀
