#!/usr/bin/env python3

import requests
import time

url = "https://example.com"  # Replace with the target URL
url = "https://ecuapass.aduana.gob.ec"

num_samples = 5  # Number of samples to take

def measure_latency(url, num_samples):
    latencies = []
    
    for _ in range(num_samples):
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            end = time.time()
            
            latency = (end - start) * 1000  # Convert to milliseconds
            latencies.append(latency)
            print(f"Sample {_ + 1}: {latency:.2f} ms")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            latencies.append(float('inf'))  # Mark as a failed request
    
    # Calculate average ignoring failed samples
    successful_latencies = [l for l in latencies if l != float('inf')]
    if successful_latencies:
        average_latency = sum(successful_latencies) / len(successful_latencies)
        print(f"Average Latency: {average_latency:.2f} ms")
        return average_latency
    else:
        print("All samples failed.")
        return None

latency = measure_latency(url, num_samples)

