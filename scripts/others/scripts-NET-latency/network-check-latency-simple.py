#!/usr/bin/env python3
import requests
import time

#url = "https://example.com"  # Replace with the target URL
url = "https://ecuapass.aduana.gob.ec"

def measure_latency(url):
    try:
        start = time.time()
        response = requests.get (url, timeout=10)
        end = time.time()
        
        latency = (end - start) * 1000  # Convert to milliseconds
        print(f"Latency: {latency:.2f} ms")
        return latency
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

latency = measure_latency (url)

