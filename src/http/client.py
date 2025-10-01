import requests
from dotenv import load_dotenv
import os
import time

load_dotenv(".env")
SERVER_URL = os.getenv("SERVER_URL")

def get_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    return None


if __name__ == "__main__":
    file = "1MB"
    times_elapsed = []

    for nums in range(100):
        start = time.time()
        data = get_data(f"http://{SERVER_URL}{file}")
        if data:
            print("Hit")
            print(f"Epoch: {nums} -- Time elapsed: {time.time() - start} seconds")
        else:
            print("Miss")
        times_elapsed.append(time.time() - start)

    print(f"Average time elapsed: {sum(times_elapsed) / len(times_elapsed)} seconds")