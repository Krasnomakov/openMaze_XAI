import requests
from requests.auth import HTTPBasicAuth
import time

url = "https://htc.gbs4u.nl/enteliweb/api/.bacnet/htc/850500"
username = "HTC_API_IMEC"  
password = "yjSJ4A$E!iyhoLp#B4dm"  

def send_get_request():
    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    while True:
        result = send_get_request()
        print(result)

        # Wait for 5 minutes before sending the next request
        time.sleep(300)

if __name__ == "__main__":
    main()
