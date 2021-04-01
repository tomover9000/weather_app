from flask import Flask
from flask import jsonify
from flask import render_template
from flask import url_for
from flask import send_from_directory
import Adafruit_DHT
from datetime import datetime
import sys

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 15
# config the path for images
app.config["CLIENT_IMAGES"] = "/home/pi/weather_app/templates/images"

with app.test_request_context():
    url_for('static', filename='style.css')
    url_for('static', filename='app.js')

@app.route('/api')
def api():
    try:
        humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        return jsonify({
            "temperature": temp,
            "humidity": humidity
        })
    except TimeoutError:
        with open("logs/errors.txt", 'w') as errors:
            print(str(datetime.now()) + ": Too many requests on the sensor", file=errors)
        return jsonify({
            "temperature": "invalid",
            "humidity": "invalid"
        })

@app.route('/')
def home():
    return render_template('./home.html')

@app.route('/get_image/<image_name>')
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)
