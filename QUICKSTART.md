# 🚀 Quick Start Guide

This guide will help you get the Turbofan RUL Prediction project up and running in minutes.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9 or higher
- ✅ pip installed
- ✅ Git installed
- ✅ Docker installed (optional, for containerization)

## 5-Minute Quick Start

### Step 1: Clone and Navigate (30 seconds)

```bash
cd /workspaces/ML/Midterm_Project/turbofan-rul-prediction
```

The project is already set up in your workspace!

### Step 2: Setup Environment (2 minutes)

```bash
# Run the automated setup script
./scripts/setup.sh
```

This will:
- ✅ Install UV package manager
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify dataset is downloaded

### Step 3: Train Model (1-2 minutes)

```bash
# Activate virtual environment
source .venv/bin/activate

# Train the model
python train.py
```

You'll see:
- Data loading progress
- Feature engineering steps
- Model training metrics
- Final test performance

### Step 4: Start Service (30 seconds)

```bash
# Start the FastAPI service
uvicorn predict:app --host 0.0.0.0 --port 8000
```

Service is now running at:
- 🌐 http://localhost:8000
- 📚 http://localhost:8000/docs (Interactive API docs)

### Step 5: Test the Service (30 seconds)

Open a new terminal:

```bash
cd /workspaces/ML/Midterm_Project/turbofan-rul-prediction
source .venv/bin/activate
python test.py
```

You should see all tests pass! ✅

## Even Faster: One-Command Start

If you want everything in one go:

```bash
# Activate environment
source .venv/bin/activate

# Train and start service
./scripts/quick_start.sh
```

## Docker Quick Start

For containerized deployment:

```bash
# Build and run with Docker
./scripts/docker_run.sh

# Service will be available at http://localhost:8000
```

## Making Your First Prediction

Once the service is running, try this:

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

Expected response:
```json
{
  "unit_id": 1,
  "predicted_rul": 112.5,
  "confidence": "medium"
}
```

## Next Steps

Now that everything is running:

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Review the Notebook**: Open `notebook.ipynb` in Jupyter
3. **Check Model Performance**: Look at the training output
4. **Read Documentation**: Check out the README.md
5. **Deploy to Cloud**: Follow deployment/README.md

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn predict:app --host 0.0.0.0 --port 8080
```

### Module Not Found

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv pip install -e .
```

### Model Files Not Found

```bash
# Retrain the model
python train.py
```

### Docker Issues

```bash
# Check Docker is running
docker ps

# Rebuild image
docker build -t turbofan-rul .
```

## Common Commands

```bash
# Activate environment
source .venv/bin/activate

# Train model
python train.py

# Start service
uvicorn predict:app --host 0.0.0.0 --port 8000

# Test service
python test.py

# Run with Docker
./scripts/docker_run.sh

# View Docker logs
docker logs turbofan-rul-prediction

# Stop Docker container
docker stop turbofan-rul-prediction
```

## File Locations

- **Dataset**: `data/CMaps/`
- **Trained Model**: `models/xgboost_rul_model.pkl`
- **Notebook**: `notebook.ipynb`
- **Scripts**: `scripts/`
- **Documentation**: `README.md`, `docs/`, `deployment/`

## Support

If you encounter issues:

1. Check the main [README.md](../README.md)
2. Review [ARCHITECTURE.md](../docs/ARCHITECTURE.md)
3. Check deployment guide in [deployment/README.md](../deployment/README.md)
4. Ensure all prerequisites are installed
5. Verify dataset is downloaded

## Success Checklist

- ✅ Virtual environment created
- ✅ Dependencies installed
- ✅ Dataset downloaded
- ✅ Model trained successfully
- ✅ Service starts without errors
- ✅ Tests pass
- ✅ Can make predictions

Congratulations! You're all set! 🎉

---

**Happy Predicting! 🚀**
