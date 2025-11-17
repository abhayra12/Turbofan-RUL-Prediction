"""
FastAPI Prediction Service for Turbofan Engine RUL Prediction

This service provides REST API endpoints for predicting
Remaining Useful Life (RUL) of turbofan engines.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Turbofan Engine RUL Prediction API",
    description="Predict Remaining Useful Life of turbofan engines using sensor data",
    version="1.0.0"
)

# Model directory
MODEL_DIR = Path('models')

# Global variables for model and artifacts
model = None
scaler = None
config = None
metadata = None

# ============================================================================
# LOAD MODEL AND ARTIFACTS
# ============================================================================

def load_model_artifacts():
    """Load model and all necessary artifacts"""
    global model, scaler, config, metadata
    
    try:
        # Load model
        with open(MODEL_DIR / 'xgboost_rul_model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.info("✓ Model loaded successfully")
        
        # Load scaler
        with open(MODEL_DIR / 'scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        logger.info("✓ Scaler loaded successfully")
        
        # Load configuration
        with open(MODEL_DIR / 'config.pkl', 'rb') as f:
            config = pickle.load(f)
        logger.info("✓ Configuration loaded successfully")
        
        # Load metadata
        with open(MODEL_DIR / 'model_metadata.pkl', 'rb') as f:
            metadata = pickle.load(f)
        logger.info("✓ Metadata loaded successfully")
        
        logger.info(f"Model type: {metadata['model_type']}")
        logger.info(f"Test RMSE: {metadata['test_rmse']:.4f}")
        logger.info(f"Number of features: {metadata['n_features']}")
        
    except Exception as e:
        logger.error(f"Error loading model artifacts: {e}")
        raise

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SensorReading(BaseModel):
    """Single sensor reading for one time cycle"""
    unit_id: int = Field(..., description="Engine unit identifier", ge=1)
    time_cycles: int = Field(..., description="Current time cycle", ge=1)
    setting_1: float = Field(..., description="Operational setting 1")
    setting_2: float = Field(..., description="Operational setting 2")
    setting_3: float = Field(..., description="Operational setting 3")
    sensor_1: float = Field(..., description="Sensor 1 reading")
    sensor_2: float = Field(..., description="Sensor 2 reading")
    sensor_3: float = Field(..., description="Sensor 3 reading")
    sensor_4: float = Field(..., description="Sensor 4 reading")
    sensor_5: float = Field(..., description="Sensor 5 reading")
    sensor_6: float = Field(..., description="Sensor 6 reading")
    sensor_7: float = Field(..., description="Sensor 7 reading")
    sensor_8: float = Field(..., description="Sensor 8 reading")
    sensor_9: float = Field(..., description="Sensor 9 reading")
    sensor_10: float = Field(..., description="Sensor 10 reading")
    sensor_11: float = Field(..., description="Sensor 11 reading")
    sensor_12: float = Field(..., description="Sensor 12 reading")
    sensor_13: float = Field(..., description="Sensor 13 reading")
    sensor_14: float = Field(..., description="Sensor 14 reading")
    sensor_15: float = Field(..., description="Sensor 15 reading")
    sensor_16: float = Field(..., description="Sensor 16 reading")
    sensor_17: float = Field(..., description="Sensor 17 reading")
    sensor_18: float = Field(..., description="Sensor 18 reading")
    sensor_19: float = Field(..., description="Sensor 19 reading")
    sensor_20: float = Field(..., description="Sensor 20 reading")
    sensor_21: float = Field(..., description="Sensor 21 reading")
    
    class Config:
        json_schema_extra = {
            "example": {
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
            }
        }

class BatchSensorReadings(BaseModel):
    """Multiple sensor readings for batch prediction"""
    readings: List[SensorReading] = Field(..., description="List of sensor readings")

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    unit_id: int
    predicted_rul: float
    confidence: str

class BatchPredictionResponse(BaseModel):
    """Response model for batch predictions"""
    predictions: List[PredictionResponse]
    total_predictions: int

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_type: str = None
    test_rmse: float = None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def add_rolling_features(df, sensor_cols, window=5):
    """Add rolling mean and std features for sensors"""
    df_roll = df.copy()
    
    for sensor in sensor_cols:
        # Rolling mean
        df_roll[f'{sensor}_rolling_mean'] = df_roll.groupby('unit_id')[sensor].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
        
        # Rolling std
        df_roll[f'{sensor}_rolling_std'] = df_roll.groupby('unit_id')[sensor].transform(
            lambda x: x.rolling(window=window, min_periods=1).std()
        )
    
    # Fill NaN in rolling std with 0
    df_roll = df_roll.fillna(0)
    
    return df_roll

def prepare_features(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare features for prediction"""
    # Add rolling features
    df_processed = add_rolling_features(data, config['top_sensors'], window=config['rolling_window'])
    
    # Select only required features
    X = df_processed[config['all_features']]
    
    return X

def get_confidence_level(rul_value: float) -> str:
    """Determine confidence level based on RUL value"""
    if rul_value < 30:
        return "high"
    elif rul_value < 80:
        return "medium"
    else:
        return "low"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("Starting up Turbofan RUL Prediction API...")
    load_model_artifacts()
    logger.info("API is ready to serve predictions!")

@app.get("/", response_model=Dict)
async def root():
    """Root endpoint"""
    return {
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

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None and scaler is not None
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        model_type=metadata.get('model_type') if model_loaded else None,
        test_rmse=metadata.get('test_rmse') if model_loaded else None
    )

@app.get("/model/info", response_model=Dict)
async def model_info():
    """Get model information"""
    if metadata is None:
        raise HTTPException(status_code=500, detail="Model metadata not loaded")
    
    return {
        "model_type": metadata.get('model_type'),
        "dataset": metadata.get('dataset'),
        "n_features": metadata.get('n_features'),
        "test_metrics": {
            "rmse": metadata.get('test_rmse'),
            "mae": metadata.get('test_mae'),
            "r2": metadata.get('test_r2')
        },
        "training_date": metadata.get('training_date'),
        "best_params": metadata.get('best_params')
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(reading: SensorReading):
    """Predict RUL for a single sensor reading"""
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert to DataFrame
        data = pd.DataFrame([reading.dict()])
        
        # Prepare features
        X = prepare_features(data)
        
        # Make prediction
        rul_pred = model.predict(X)[0]
        
        # Ensure non-negative RUL
        rul_pred = max(0, rul_pred)
        
        # Get confidence
        confidence = get_confidence_level(rul_pred)
        
        return PredictionResponse(
            unit_id=reading.unit_id,
            predicted_rul=float(rul_pred),
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(batch: BatchSensorReadings):
    """Predict RUL for multiple sensor readings"""
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert to DataFrame
        data = pd.DataFrame([reading.dict() for reading in batch.readings])
        
        # Prepare features
        X = prepare_features(data)
        
        # Make predictions
        rul_preds = model.predict(X)
        
        # Ensure non-negative RUL
        rul_preds = np.maximum(0, rul_preds)
        
        # Create response
        predictions = []
        for idx, reading in enumerate(batch.readings):
            predictions.append(PredictionResponse(
                unit_id=reading.unit_id,
                predicted_rul=float(rul_preds[idx]),
                confidence=get_confidence_level(rul_preds[idx])
            ))
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_predictions=len(predictions)
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/ping")
async def ping():
    """Simple ping endpoint for health monitoring"""
    return {"status": "ok"}

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
