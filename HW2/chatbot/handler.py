import datetime
import requests
import random

# Function to call the figlet service with the given text
def invoke_figlet(text):
    figlet_response = requests.post("http://192.168.64.2:8080/function/figlet", data=text)
    if figlet_response.status_code == 200:
        return figlet_response.text
    else:
        return "Oops!! An error calling the figlet service."

def handle(req):
    # Convert the input string to lowercase for case-insensitive matching
    normalized_input = req.lower()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if 'figlet for name' in normalized_input:
        return invoke_figlet("name")
    elif 'figlet for date' in normalized_input:
        return invoke_figlet("date")
    elif 'figlet for time' in normalized_input:
        return invoke_figlet("time")
    elif 'name' in normalized_input:
        names = ["Chat Assistant", "Silvi", "Chatbot"]
        return random.choice(["I'm called as {}.".format(names[1]),
                              "I'm your personal {}.".format(names[0]),
                              "I go by the name {}.".format(names[2])])
    elif 'date' in normalized_input or 'time' in normalized_input:
        return random.choice(["The clock shows {}.".format(current_time),
                              "It's currently {}.".format(current_time),
                              "Current date and time is {}.".format(current_time)])
    elif 'figlet' in normalized_input:
        start_index = normalized_input.find("for ")
        if start_index != -1:
            figlet_text = normalized_input[start_index + 4:].strip()
            if figlet_text:
                return invoke_figlet(figlet_text)
            else:
                return "What text would you like me to tranform to the figlet."
        else:
            return "Could you specify the text for the figlet."
    else:
        return "I'm not sure how to respond to that, Sorry!!"