from datetime import datetime, time
import requests
import uuid
import os 
from dotenv import load_dotenv


GOVEE_API_KEY = os.getenv("GOVEE_API_KEY")
GOVEE_DEVICE_ID = "YOUR_DEVICE_ID_HERE"  
GOVEE_SKU = "YOUR_SKU_HERE"
GOVEE_API_URL = "https://openapi.api.govee.com/router/api/v1/device/control"

def main():
    if validateLight():
        print("Time is valid (10:00 AM - 11:00 PM). Turning light ON...")
        control_light(1)  # 1 = on
    else:
        print("Time is outside valid range. Turning light OFF...")
        control_light(0)  # 0 = off

def validateLight() -> bool:
    now = datetime.now().time()
    earliest = time(10, 0)
    latest = time(23, 0)
    return earliest <= now <= latest

def control_light(value: int):
  
    headers = {
        "Govee-API-Key": GOVEE_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "requestId": str(uuid.uuid4()),
        "payload": {
            "sku": GOVEE_SKU,
            "device": GOVEE_DEVICE_ID,
            "capability": {
                "type": "devices.capabilities.toggle",
                "instance": "powerSwitch",
                "value": value
            }
        }
    }
    
    try:
        response = requests.post(GOVEE_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"Successfully sent command. Response: {response.json()}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()

