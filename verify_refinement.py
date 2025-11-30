import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(name, url, data):
    print(f"Testing {name}...")
    try:
        response = requests.post(f"{BASE_URL}{url}", json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"  [PASS] {name}: {json.dumps(result['result'], indent=2)}")
                return True
            else:
                print(f"  [FAIL] {name}: {result.get('error')}")
        else:
            print(f"  [FAIL] {name}: Status {response.status_code}")
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
    return False

def test_supplier_search():
    print("Testing Real Supplier Search...")
    try:
        data = {"part_number": "LC1D09M7"} # Real Schneider part
        response = requests.post(f"{BASE_URL}/api/suppliers/search", json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('components'):
                comp = result['components'][0]
                print(f"  [PASS] Found Real Component: {comp['manufacturer']} {comp['part_number']}")
                print(f"         Price: ${comp['price']:.2f} (Live Scraped)")
                return True
            else:
                print(f"  [FAIL] Supplier Search: {result.get('error')}")
        else:
            print(f"  [FAIL] Supplier Search: Status {response.status_code}")
    except Exception as e:
        print(f"  [FAIL] Supplier Search: {e}")
    return False

def main():
    print("=== Verifying Refined Application ===")
    
    # Wait for app to reload if needed
    time.sleep(2)
    
    # 1. Voltage Drop
    test_endpoint("Voltage Drop", "/api/calculate/voltage-drop", {
        "voltage": 480, "current": 50, "distance_ft": 200, "conductor_size": "6"
    })
    
    # 2. Fault Current
    test_endpoint("Fault Current", "/api/calculate/fault-current", {
        "source_voltage": 480, "transformer_kva": 1000, "transformer_impedance": 5.75
    })
    
    # 3. Cable Sizing
    test_endpoint("Cable Sizing", "/api/calculate/cable-sizing", {
        "current_amps": 100, "voltage": 480
    })
    
    # 4. Breaker Sizing
    test_endpoint("Breaker Sizing", "/api/calculate/breaker-sizing", {
        "load_amps": 45, "load_type": "continuous"
    })
    
    # 5. Motor Startup
    test_endpoint("Motor Startup", "/api/calculate/motor-startup", {
        "motor_hp": 50, "voltage": 480, "method": "soft_start"
    })
    
    # 6. Real Supplier Search
    test_supplier_search()

if __name__ == "__main__":
    main()
