import requests
import time

def send_request(input_data):
    start_time = time.time()
    response = requests.post("http://192.168.64.2:8080/function/figlet", data=input_data)
    end_time = time.time()
    response_time = end_time - start_time
    return response, response_time

# Test Scenario 1
input_data = "What is your name?"
response, response_time = send_request(input_data)
print("Test Scenario 1 - Response Time for the First Request that Does Not Call Figlet:")
# print("Response:", response.text)
print("Response Time:", response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 2
input_data = "What time is it?"
response, response_time = send_request(input_data)
print("Test Scenario 2 - Response Time for the Second Request that Does Not Call Figlet:")
# print("Response:", response.text)
print("Response Time:", response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 3
total_response_time = 0
for _ in range(10):
    input_data = "What is your name?"
    _, response_time = send_request(input_data)
    total_response_time += response_time
average_response_time = total_response_time / 10
print("Test Scenario 3 - Average Response Time Over 10 Requests that Do Not Call Figlet:")
print("Average Response Time:", average_response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 4
input_data = "figlet for Silvi"
response, response_time = send_request(input_data)
print("Test Scenario 4 - Response Time for the First Request that Calls Figlet:")
print("Response:", response.text)
print("Response Time:", response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 5
input_data = "figlet for Silvi"
_, _ = send_request(input_data)  
response, response_time = send_request(input_data)
print("Test Scenario 5 - Response Time for the Second Request that Calls Figlet:")
print("Response:", response.text)
print("Response Time:", response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 6
input_data = "What is your name?"  
_, _ = send_request(input_data)  
input_data = "figlet for Silvi"  
response, response_time = send_request(input_data)
print("Test Scenario 6 - Response Time for the Second Request that Calls Figlet Following the First Request that Does Not Call Figlet:")
print("Response:", response.text)
print("Response Time:", response_time, "seconds")
print("******************************************************************************************")
print()

# Test Scenario 7
total_response_time = 0
for _ in range(10):
    input_data = "figlet for Silvi"
    _, response_time = send_request(input_data)
    total_response_time += response_time
average_response_time = total_response_time / 10
print("Test Scenario 7 - Average Response Time Over 10 Requests that Call Figlet:")
print("Average Response Time:", average_response_time, "seconds")