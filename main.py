#This Python code runs a website that lets you check the time in any city of interest. It uses the TimeZoneDB API, so you must register and obtain an API key before running the code.
#A list of available cities can be found at: https://timezonedb.com/time-zones
#Enjoy

from flask import Flask, request, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "ADD_YOUR_TIMEZONEDB_API_KEY"  # Replace with your actual API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-time', methods=['POST'])
def get_time():
    city = request.form.get('city')
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone={city}"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "formatted" not in data:
            return render_template('index.html', message="That city cannot be found")
        if data["status"] == "FAILED":
            time_info = f"That city cannot be found!"
        else:
            time_info = f"Current time in {data['zoneName']}: {data['formatted']}"
        return render_template('index.html', time_info=time_info)

    except Exception as e:
        print("Server error:", e)
        return render_template('index.html', message="Server error")

if __name__ == '__main__':
    app.run(debug=True)
