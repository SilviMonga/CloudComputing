import argparse
import requests
import threading
import time

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'HUjjzo9NWK4weGRDYTxnTroqGLmZeBuMso5jXkfbfi2BKX1bY2Zi8b2z3IqLgT1'
DEFAULT_RATE = 10
DEFAULT_DURATION = 60
MAX_REPLICAS = 10

def send_request(input_data):
    url = f"http://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@192.168.64.2:8080/functions/chatbot"
    response = requests.post(url, data=input_data)
    return response

def get_replica_count():
    url = f"http://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@192.168.64.2:8080/system/functions"
    response = requests.get(url)
    functions = response.json()
    for function in functions:
        if function["name"] == "chatbot":
            return function["replicas"]
    return 0

def scale_replicas(replicas):
    url = f"http://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@192.168.64.2:8080/system/functions/chatbot"
    data = {"replicas": replicas}
    requests.post(url, json=data)

def send_parallel_requests(input_data, rate=DEFAULT_RATE, duration=DEFAULT_DURATION):
    start_time = time.time()
    end_time = start_time + duration
    request_count = 0

    while time.time() < end_time:
        start_time_request = time.time()
        threads = []

        for _ in range(rate):
            thread = threading.Thread(target=send_request, args=(input_data,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            request_count += 1

        elapsed_time_request = time.time() - start_time_request
        time.sleep(max(0, 1 - elapsed_time_request))  # Ensure rate of requests

        current_replicas = get_replica_count()
        served_requests = request_count
        print(f"Current replica count: {current_replicas}, Served requests: {served_requests}")

        if request_count > 100:
            if current_replicas < MAX_REPLICAS:
                print(f"Request count exceeded 100. Scaling up replicas...")
                scale_replicas(current_replicas + 1)
                print(f"Current replica count after scaling: {current_replicas + 1}")
        with open("scaling_log.txt", "a") as log_file:  # Open the file in append mode
            log_file.write(f"Current replica count: {current_replicas}, Served requests: {served_requests}\n")

    elapsed_time = time.time() - start_time
    total_requests = rate * duration
    queries_per_second = total_requests / elapsed_time
    print(f"Queries Per Second: {queries_per_second:.2f}")
    with open("scaling_log.txt", "a") as log_file:  # Open the file in append mode
        log_file.write(f"Queries Per Second: {queries_per_second:.2f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send parallel requests to the OpenFaaS function")
    parser.add_argument("input_data", type=str, help="Input data for the requests")
    parser.add_argument("--rate", type=int, default=DEFAULT_RATE, help="Rate of requests per second")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION, help="Duration of the test in seconds")
    args = parser.parse_args()

    input_data = args.input_data
    rate = args.rate
    duration = args.duration

    send_parallel_requests(input_data, rate, duration)