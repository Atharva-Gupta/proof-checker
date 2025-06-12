#!/usr/bin/env python3

import requests
import json

# Test the web API
def test_proof_checker_api():
    url = "http://127.0.0.1:5000/check-proof"
    
    # Test 1: Valid simple proof
    test_proof_1 = """[p, q] |- (p \\and q) :AI
[(p \\and q)] |- p :AE"""
    
    response = requests.post(url, json={"proof": test_proof_1})
    print("Test 1 - Valid proof:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Test 2: Invalid proof
    test_proof_2 = """[p] |- q :AX"""
    
    response = requests.post(url, json={"proof": test_proof_2})
    print("Test 2 - Invalid proof:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Test 3: Parse error
    test_proof_3 = """invalid format"""
    
    response = requests.post(url, json={"proof": test_proof_3})
    print("Test 3 - Parse error:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    try:
        test_proof_checker_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server.")
        print("Make sure to run 'python3 app.py' first!")