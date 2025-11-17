"""
Test script for the prediction service

This script tests the FastAPI prediction service locally.
"""

import requests
import json

# Base URL (change if running on different host/port)
BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("\n" + "="*80)
    print("Testing Root Endpoint")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Root endpoint failed"
    print("✓ Root endpoint test passed")

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*80)
    print("Testing Health Check Endpoint")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed"
    assert response.json()["model_loaded"] == True, "Model not loaded"
    print("✓ Health check test passed")

def test_model_info():
    """Test model info endpoint"""
    print("\n" + "="*80)
    print("Testing Model Info Endpoint")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Model info failed"
    print("✓ Model info test passed")

def test_single_prediction():
    """Test single prediction"""
    print("\n" + "="*80)
    print("Testing Single Prediction")
    print("="*80)
    
    # Sample sensor reading
    sample_data = {
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
    
    response = requests.post(f"{BASE_URL}/predict", json=sample_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Single prediction failed"
    assert "predicted_rul" in response.json(), "No RUL in response"
    print(f"✓ Single prediction test passed")
    print(f"  Predicted RUL: {response.json()['predicted_rul']:.2f} cycles")
    print(f"  Confidence: {response.json()['confidence']}")

def test_batch_prediction():
    """Test batch prediction"""
    print("\n" + "="*80)
    print("Testing Batch Prediction")
    print("="*80)
    
    # Sample batch data (2 readings)
    batch_data = {
        "readings": [
            {
                "unit_id": 1,
                "time_cycles": 50,
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
            },
            {
                "unit_id": 2,
                "time_cycles": 150,
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
        ]
    }
    
    response = requests.post(f"{BASE_URL}/predict/batch", json=batch_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Batch prediction failed"
    assert response.json()["total_predictions"] == 2, "Wrong number of predictions"
    print("✓ Batch prediction test passed")

def test_ping():
    """Test ping endpoint"""
    print("\n" + "="*80)
    print("Testing Ping Endpoint")
    print("="*80)
    
    response = requests.get(f"{BASE_URL}/ping")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Ping failed"
    print("✓ Ping test passed")

def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("TURBOFAN RUL PREDICTION SERVICE - TEST SUITE")
    print("="*80)
    print(f"Testing service at: {BASE_URL}")
    
    try:
        test_root()
        test_health()
        test_model_info()
        test_ping()
        test_single_prediction()
        test_batch_prediction()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the service")
        print(f"   Make sure the service is running at {BASE_URL}")
        print("   Run: uvicorn predict:app --host 0.0.0.0 --port 8000")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    main()
