from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.Timeout:
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    unique_numbers = set()

    for url in urls:
        numbers = fetch_numbers_from_url(url)
        unique_numbers.update(numbers)

    merged_numbers = sorted(unique_numbers)
    return jsonify(numbers=merged_numbers)

if __name__ == '__main__':
    app.run(debug=True)
