from flask import Flask, request, jsonify
import requests
from datetime import datetime


app = Flask(__name__)

# Replace these with your registered credentials
CLIENT_ID = "b46118f0-fbde-4b16-a4b1-6ae6ad718b27"
CLIENT_SECRET = "XOyolORPasKWODAN"
BASE_URL = "http://20.244.56.144"

def get_access_token():
    auth_data = {
        "companyName": "Train Central",
        "clientID": CLIENT_ID,
        "ownerName": "Rahul",
        "ownerEmail": "rahul@abc.edu",
        "rollNo": "1",
        "clientSecret": CLIENT_SECRET
    }
    response = requests.post(f"{BASE_URL}/train/auth", json=auth_data)
    return response.json().get("access_token")

def get_trains(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/train/trains", headers=headers)
    return response.json()

@app.route("/trains", methods=["GET"])
def get_train_schedule():
    access_token = get_access_token()
    trains = get_trains(access_token)
    
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    
    filtered_trains = [
        train for train in trains
        if (
            train["departureTime"]["Hours"] > current_hour or
            (train["departureTime"]["Hours"] == current_hour and train["departureTime"]["Minutes"] > current_minute + 30)
        )
    ]
    
    sorted_trains = sorted(
        filtered_trains,
        key=lambda x: (x["price"]["AC"], -x["seatsAvailable"]["AC"], -x["delayedBy"], x["departureTime"]["Hours"], x["departureTime"]["Minutes"])
    )
    
    return jsonify(sorted_trains)

if __name__ == "__main__":
    app.debug = False
    app.run()

