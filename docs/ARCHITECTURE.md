# Architecture Diagrams

This document contains ASCII-based architecture diagrams for the Turbofan RUL Prediction system.

## 1. Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TURBOFAN RUL PREDICTION SYSTEM                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌───────────────────┐         ┌───────────────────┐         ┌───────────────┐
│                   │         │                   │         │               │
│   NASA C-MAPSS    │────────▶│   Data Pipeline   │────────▶│   Feature     │
│     Dataset       │         │   (Loading & EDA) │         │  Engineering  │
│                   │         │                   │         │               │
└───────────────────┘         └───────────────────┘         └───────┬───────┘
                                                                     │
                                                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MODEL TRAINING PIPELINE                           │
│                                                                              │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────┐   ┌────────────┐ │
│  │   Linear    │   │    Ridge     │   │ Random Forest  │   │  Gradient  │ │
│  │ Regression  │   │  Regression  │   │   Regressor    │   │  Boosting  │ │
│  └─────────────┘   └──────────────┘   └────────────────┘   └────────────┘ │
│                                                                              │
│  ┌─────────────┐   ┌──────────────────────────────────────────────────┐    │
│  │   XGBoost   │──▶│      Hyperparameter Tuning (GridSearchCV)        │    │
│  │  Regressor  │   │              ↓                                   │    │
│  └─────────────┘   │        Best Model Selection                      │    │
│                    └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┬───────────────────────────┘
                                                   │
                                                   ▼
                                         ┌──────────────────┐
                                         │  Model Artifacts │
                                         │  ================│
                                         │  • model.pkl     │
                                         │  • scaler.pkl    │
                                         │  • config.pkl    │
                                         │  • metadata.pkl  │
                                         └────────┬─────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT LAYER                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                    FastAPI Web Service                             │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │    │
│  │  │  /predict    │  │ /predict/    │  │  /health  /docs      │    │    │
│  │  │  (Single)    │  │   batch      │  │  (Monitoring)        │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                   │                                         │
│                                   ▼                                         │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                       Docker Container                              │    │
│  │                  (Python 3.11 + Dependencies)                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────┬───────────────────────────────────┘
                                          │
                                          ▼
                              ┌────────────────────────┐
                              │   GCP Cloud Run        │
                              │   ================     │
                              │   • Auto-scaling       │
                              │   • Load balancing     │
                              │   • HTTPS endpoint     │
                              └────────────────────────┘
                                          │
                                          ▼
                              ┌────────────────────────┐
                              │    End Users /         │
                              │  Client Applications   │
                              └────────────────────────┘
```

## 2. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            DATA FLOW                                     │
└─────────────────────────────────────────────────────────────────────────┘

Step 1: DATA INGESTION
───────────────────────
┌──────────────────┐
│  Raw Data Files  │
│  ──────────────  │
│  • train_FD*.txt │
│  • test_FD*.txt  │
│  • RUL_FD*.txt   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│   Parse & Load (pandas)          │
│   • 26 columns                   │
│   • Time series per engine       │
└────────┬─────────────────────────┘
         │
         ▼

Step 2: FEATURE ENGINEERING
────────────────────────────
┌──────────────────────────────────┐
│  Calculate RUL                   │
│  • Training: max_cycle - current │
│  • Testing: truth + remaining    │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Remove Low Variance Features    │
│  • Variance threshold: 0.01      │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Add Rolling Features            │
│  • Window size: 5                │
│  • Rolling mean & std            │
│  • Top 5 sensors                 │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Feature Scaling                 │
│  • StandardScaler                │
│  • Fit on training data          │
└────────┬─────────────────────────┘
         │
         ▼

Step 3: MODEL TRAINING
───────────────────────
┌──────────────────────────────────┐
│  Train Multiple Models           │
│  • Linear Regression             │
│  • Ridge Regression              │
│  • Random Forest                 │
│  • Gradient Boosting             │
│  • XGBoost                       │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Hyperparameter Tuning           │
│  • GridSearchCV                  │
│  • Cross-validation (3-fold)     │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Select Best Model               │
│  • Based on validation RMSE      │
└────────┬─────────────────────────┘
         │
         ▼

Step 4: MODEL PERSISTENCE
──────────────────────────
┌──────────────────────────────────┐
│  Save Artifacts                  │
│  • model.pkl                     │
│  • scaler.pkl                    │
│  • config.pkl                    │
│  • metadata.pkl                  │
└────────┬─────────────────────────┘
         │
         ▼

Step 5: PREDICTION PIPELINE
────────────────────────────
┌──────────────────────────────────┐
│  Input: Sensor Readings          │
│  • JSON payload via API          │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Feature Processing              │
│  • Calculate rolling features    │
│  • Select required features      │
│  • Apply scaling                 │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Model Inference                 │
│  • XGBoost prediction            │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Output: RUL Prediction          │
│  • Predicted cycles remaining    │
│  • Confidence level              │
└──────────────────────────────────┘
```

## 3. API Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FASTAPI SERVICE ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │    Client    │
                              └──────┬───────┘
                                     │
                                     │ HTTP/HTTPS
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                    ▼                ▼                ▼
            ┌───────────┐    ┌──────────┐    ┌──────────────┐
            │    GET    │    │   POST   │    │     GET      │
            │  /health  │    │ /predict │    │ /model/info  │
            └─────┬─────┘    └────┬─────┘    └──────┬───────┘
                  │               │                  │
                  └───────────────┼──────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
         ┌─────────────────────┐    ┌──────────────────────┐
         │   Health Check      │    │  Prediction Logic    │
         │   ─────────────     │    │  ─────────────────   │
         │   • Model loaded?   │    │  1. Validate input   │
         │   • Service status  │    │  2. Process features │
         └─────────────────────┘    │  3. Load model       │
                                    │  4. Make prediction  │
                                    │  5. Format response  │
                                    └──────────┬───────────┘
                                               │
                    ┌──────────────────────────┼────────────────┐
                    │                          │                │
                    ▼                          ▼                ▼
         ┌─────────────────┐      ┌─────────────────┐  ┌──────────────┐
         │   Model Layer   │      │  Feature Layer  │  │ Validation   │
         │   ───────────   │      │  ─────────────  │  │ Layer        │
         │   • XGBoost     │      │  • Rolling      │  │ ────────     │
         │   • Scaler      │      │    features     │  │ • Pydantic   │
         │   • Config      │      │  • Scaling      │  │   models     │
         └─────────────────┘      └─────────────────┘  └──────────────┘
                    │                          │                │
                    └──────────────────────────┼────────────────┘
                                               │
                                               ▼
                                    ┌──────────────────┐
                                    │  JSON Response   │
                                    │  ──────────────  │
                                    │  • unit_id       │
                                    │  • predicted_rul │
                                    │  • confidence    │
                                    └──────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                            API ENDPOINTS                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  GET  /              - Root endpoint (API info)                         │
│  GET  /health        - Health check                                     │
│  GET  /ping          - Simple ping                                      │
│  GET  /model/info    - Model metadata                                   │
│  GET  /docs          - OpenAPI documentation                            │
│  POST /predict       - Single prediction                                │
│  POST /predict/batch - Batch predictions                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 4. Deployment Architecture (GCP Cloud Run)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      GCP CLOUD RUN DEPLOYMENT                            │
└─────────────────────────────────────────────────────────────────────────┘

DEVELOPMENT ENVIRONMENT
───────────────────────
┌──────────────────────┐
│  Local Development   │
│  ───────────────────│
│  1. Code changes     │
│  2. Test locally     │
│  3. Commit to Git    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────┐
│     Container Registry           │
│     ─────────────────            │
│  gcr.io/project-id/image:tag     │
└──────────┬───────────────────────┘
           │
           ▼

CLOUD INFRASTRUCTURE
────────────────────
┌─────────────────────────────────────────────────────────────────┐
│                        GCP Project                              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │              Cloud Run Service                         │    │
│  │                                                        │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │ Instance │  │ Instance │  │ Instance │  (Auto-   │    │
│  │  │    1     │  │    2     │  │    N     │   scale)  │    │
│  │  └──────────┘  └──────────┘  └──────────┘           │    │
│  │       │              │              │                │    │
│  │       └──────────────┴──────────────┘                │    │
│  │                      │                               │    │
│  │              ┌───────┴────────┐                      │    │
│  │              │ Load Balancer  │                      │    │
│  │              └───────┬────────┘                      │    │
│  └──────────────────────┼───────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────┼───────────────────────────────┐    │
│  │              Cloud Logging & Monitoring              │    │
│  │              ───────────────────────────             │    │
│  │              • Request logs                          │    │
│  │              • Error tracking                        │    │
│  │              • Performance metrics                   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            │ HTTPS
                            │
                            ▼
                ┌──────────────────────┐
                │  Internet / Clients  │
                └──────────────────────┘

SCALING BEHAVIOR
────────────────
Traffic │ Instances
  Low   │    0-1     (scales to zero)
 Medium │    1-3
  High  │    3-10    (max instances)
```

## 5. CI/CD Pipeline (Conceptual)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CI/CD PIPELINE                                  │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Git Push   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Git Repository  │
└──────┬───────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Build Stage                  │
│        ────────────                 │
│  • Install dependencies             │
│  • Run linters (flake8, black)      │
│  • Run tests (pytest)               │
└──────┬──────────────────────────────┘
       │
       │ ✓ Tests Pass
       ▼
┌─────────────────────────────────────┐
│        Docker Build                 │
│        ────────────                 │
│  • Build image                      │
│  • Tag with version                 │
│  • Push to registry                 │
└──────┬──────────────────────────────┘
       │
       │ ✓ Build Success
       ▼
┌─────────────────────────────────────┐
│        Deploy Stage                 │
│        ────────────                 │
│  • Deploy to Cloud Run              │
│  • Run health checks                │
│  • Monitor deployment               │
└──────┬──────────────────────────────┘
       │
       │ ✓ Deploy Success
       ▼
┌─────────────────────────────────────┐
│        Production                   │
│        ──────────                   │
│  • Service live                     │
│  • Monitoring active                │
│  • Logs collected                   │
└─────────────────────────────────────┘
```

## 6. Model Training Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MODEL TRAINING WORKFLOW                             │
└─────────────────────────────────────────────────────────────────────────┘

 ┌─────────────┐
 │ Raw Dataset │
 └──────┬──────┘
        │
        ├──────────────────────┬──────────────────────┬─────────────────┐
        │                      │                      │                 │
        ▼                      ▼                      ▼                 ▼
  ┌──────────┐         ┌──────────┐          ┌──────────┐      ┌──────────┐
  │   EDA    │         │  Clean   │          │ Feature  │      │  Split   │
  │          │────────▶│   Data   │─────────▶│   Eng    │─────▶│   Data   │
  └──────────┘         └──────────┘          └──────────┘      └──────────┘
                                                                      │
        ┌─────────────────────────────────────────────────────────────┘
        │
        ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                     MODEL TRAINING                                │
  │                                                                   │
  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐│
  │  │  Linear    │  │   Ridge    │  │  Random    │  │  Gradient  ││
  │  │ Regression │  │ Regression │  │  Forest    │  │  Boosting  ││
  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘│
  │        └────────────────┴───────────────┴────────────────┘      │
  │                              │                                   │
  │                              ▼                                   │
  │                      ┌────────────────┐                          │
  │                      │    XGBoost     │                          │
  │                      │   + Tuning     │                          │
  │                      └────────┬───────┘                          │
  └─────────────────────────────────┼─────────────────────────────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │ Model Evaluation │
                          │ ──────────────── │
                          │ • RMSE           │
                          │ • MAE            │
                          │ • R²             │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Best Model      │
                          │  Selection       │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Save Artifacts  │
                          │  • model.pkl     │
                          │  • scaler.pkl    │
                          │  • config.pkl    │
                          └──────────────────┘
```

---

**Note**: These are ASCII-based diagrams. For presentation purposes, you can create more polished diagrams using tools like:
- Draw.io (diagrams.net)
- Lucidchart
- Microsoft Visio
- PlantUML
- Mermaid

For web-based architecture diagrams with icons:
- Cloudcraft (for AWS)
- GCP Architecture Diagramming Tool
- Azure Architecture Icons
