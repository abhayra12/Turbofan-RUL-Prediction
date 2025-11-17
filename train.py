"""
Train XGBoost Model for Turbofan Engine RUL Prediction

This script trains the final model on the NASA C-MAPSS dataset
and saves the model and necessary artifacts for deployment.
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Constants
RANDOM_SEED = 42
DATA_DIR = Path('data/CMaps')
MODEL_DIR = Path('models')
DATASET = 'FD001'  # Using FD001 for simplicity

# Ensure model directory exists
MODEL_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("TURBOFAN ENGINE RUL PREDICTION - MODEL TRAINING")
print("=" * 80)

# ============================================================================
# 1. DATA LOADING
# ============================================================================
print("\n[1/7] Loading data...")

# Define column names
index_names = ['unit_id', 'time_cycles']
setting_names = ['setting_1', 'setting_2', 'setting_3']
sensor_names = [f'sensor_{i}' for i in range(1, 22)]
col_names = index_names + setting_names + sensor_names

# Load datasets
train_df = pd.read_csv(DATA_DIR / f'train_{DATASET}.txt', sep='\\s+', header=None, names=col_names)
test_df = pd.read_csv(DATA_DIR / f'test_{DATASET}.txt', sep='\\s+', header=None, names=col_names)
truth_df = pd.read_csv(DATA_DIR / f'RUL_{DATASET}.txt', sep='\\s+', header=None, names=['RUL'])

print(f"✓ Training data: {train_df.shape}")
print(f"✓ Test data: {test_df.shape}")
print(f"✓ Ground truth: {truth_df.shape}")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================
print("\n[2/7] Feature engineering...")

# Calculate RUL for training data
train_df['RUL'] = train_df.groupby('unit_id')['time_cycles'].transform('max') - train_df['time_cycles']

# Calculate RUL for test data
test_max_cycles = test_df.groupby('unit_id')['time_cycles'].max().reset_index()
test_max_cycles.columns = ['unit_id', 'max_cycle']
test_max_cycles['RUL_at_end'] = truth_df['RUL'].values
test_df = test_df.merge(test_max_cycles, on='unit_id', how='left')
test_df['RUL'] = test_df['RUL_at_end'] + (test_df['max_cycle'] - test_df['time_cycles'])
test_df = test_df.drop(['max_cycle', 'RUL_at_end'], axis=1)

print(f"✓ RUL calculated for training and test data")

# Identify low variance features
feature_cols = setting_names + sensor_names
variance_threshold = 0.01
variances = train_df[feature_cols].var()
low_variance_features = variances[variances < variance_threshold].index.tolist()
features_to_keep = [f for f in feature_cols if f not in low_variance_features]

print(f"✓ Removed {len(low_variance_features)} low variance features")
print(f"✓ Keeping {len(features_to_keep)} features")

# Calculate correlations and select top sensors for rolling features
correlations = train_df[features_to_keep + ['RUL']].corr()['RUL'].drop('RUL').abs().sort_values(ascending=False)
top_sensors = correlations.head(5).index.tolist()
print(f"✓ Top sensors for rolling features: {top_sensors}")

# Add rolling features
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

train_df_eng = add_rolling_features(train_df, top_sensors, window=5)
test_df_eng = add_rolling_features(test_df, top_sensors, window=5)

print(f"✓ Added rolling features (window=5)")

# Define all features
rolling_features = [col for col in train_df_eng.columns if 'rolling' in col]
all_features = features_to_keep + rolling_features

print(f"✓ Total features for modeling: {len(all_features)}")

# ============================================================================
# 3. DATA PREPARATION
# ============================================================================
print("\n[3/7] Preparing data...")

X_train = train_df_eng[all_features]
y_train = train_df_eng['RUL']
X_test = test_df_eng[all_features]
y_test = test_df_eng['RUL']

print(f"✓ Training set: {X_train.shape}")
print(f"✓ Test set: {X_test.shape}")

# ============================================================================
# 4. FEATURE SCALING
# ============================================================================
print("\n[4/7] Scaling features...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✓ Features scaled using StandardScaler")

# ============================================================================
# 5. MODEL TRAINING
# ============================================================================
print("\n[5/7] Training XGBoost model...")

# Best parameters (from hyperparameter tuning)
# You can adjust these based on your tuning results
best_params = {
    'n_estimators': 200,
    'max_depth': 5,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'random_state': RANDOM_SEED,
    'n_jobs': -1
}

model = XGBRegressor(**best_params)
model.fit(X_train, y_train)

print("✓ Model training completed")

# ============================================================================
# 6. MODEL EVALUATION
# ============================================================================
print("\n[6/7] Evaluating model...")

# Training predictions
y_train_pred = model.predict(X_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_mae = mean_absolute_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

# Test predictions
y_test_pred = model.predict(X_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_mae = mean_absolute_error(y_test, y_test_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("\n" + "=" * 80)
print("MODEL PERFORMANCE")
print("=" * 80)
print(f"\nTraining Metrics:")
print(f"  RMSE: {train_rmse:.4f}")
print(f"  MAE:  {train_mae:.4f}")
print(f"  R²:   {train_r2:.4f}")

print(f"\nTest Metrics:")
print(f"  RMSE: {test_rmse:.4f}")
print(f"  MAE:  {test_mae:.4f}")
print(f"  R²:   {test_r2:.4f}")
print("=" * 80)

# ============================================================================
# 7. SAVE MODEL AND ARTIFACTS
# ============================================================================
print("\n[7/7] Saving model and artifacts...")

# Save the model
with open(MODEL_DIR / 'xgboost_rul_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print(f"✓ Model saved to {MODEL_DIR / 'xgboost_rul_model.pkl'}")

# Save the scaler
with open(MODEL_DIR / 'scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
print(f"✓ Scaler saved to {MODEL_DIR / 'scaler.pkl'}")

# Save feature names
with open(MODEL_DIR / 'feature_names.pkl', 'wb') as f:
    pickle.dump(all_features, f)
print(f"✓ Feature names saved to {MODEL_DIR / 'feature_names.pkl'}")

# Save model metadata
metadata = {
    'model_type': 'XGBoost',
    'dataset': DATASET,
    'n_features': len(all_features),
    'features': all_features,
    'low_variance_features': low_variance_features,
    'top_sensors': top_sensors,
    'best_params': best_params,
    'train_rmse': float(train_rmse),
    'train_mae': float(train_mae),
    'train_r2': float(train_r2),
    'test_rmse': float(test_rmse),
    'test_mae': float(test_mae),
    'test_r2': float(test_r2),
    'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
}

with open(MODEL_DIR / 'model_metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)
print(f"✓ Metadata saved to {MODEL_DIR / 'model_metadata.pkl'}")

# Save configuration for prediction service
config = {
    'features_to_keep': features_to_keep,
    'top_sensors': top_sensors,
    'rolling_window': 5,
    'all_features': all_features
}

with open(MODEL_DIR / 'config.pkl', 'wb') as f:
    pickle.dump(config, f)
print(f"✓ Configuration saved to {MODEL_DIR / 'config.pkl'}")

print("\n" + "=" * 80)
print("✅ TRAINING COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\nModel artifacts saved in: {MODEL_DIR.absolute()}")
print("\nYou can now use the model for predictions using predict.py")
