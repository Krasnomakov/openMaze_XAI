import requests
from requests.auth import HTTPBasicAuth
import time
from flask import Flask, jsonify
import json

app_data = Flask(__name__)

# HTC API credentials
url = "https://htc.gbs4u.nl/enteliweb/api/.bacnet/htc/850500"
username = "HTC_API_IMEC"  
password = "yjSJ4A$E!iyhoLp#B4dm"

# File to save context data
data_file_path = "context_data.json"

# Placeholder data, replace with your actual logic to fetch data
data = {"context": "This is placeholder context data."}

def send_get_request():
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def save_to_file(data_to_save):
    with open(data_file_path, "w") as file:
        file.write(data_to_save)

def get_data():
    while True:
        result = send_get_request()
        data["context"] = result

        # Save data to the file
        save_to_file(json.dumps(data))

        # Wait for 5 minutes before sending the next request
        time.sleep(300)

@app_data.route("/get_data", methods=["GET"])
def provide_data():
    return jsonify(data)

if __name__ == "__main__":
    # Start the data fetching process in a separate thread
    from threading import Thread

    data_fetch_thread = Thread(target=get_data)
    data_fetch_thread.start()

    # Run the Flask app to provide data
    app_data.run(port=5002, debug=True)
