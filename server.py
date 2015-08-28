from flask import Flask, render_template, request, jsonify
from TED5000 import TED5000
import Pins
#import Display
import json
import os
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
ted = TED5000()

@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/_poolpump")
def _poolpump():
    state = request.args.get('state')
    if state=="on":
        Pins.PoolPumpon()
    else:
        Pins.PoolPumpoff()
    return ""

@app.route("/_pondpump")	
def _pondpump():
    state = request.args.get('state')
    if state=="on":
        Pins.LEDon()
    else:
        Pins.LEDoff()
    return ""

@app.route("/_poolpumpstatus")
def _poolpumpstatus():
    if Pins.ReadPoolPump():
        state = "off"
    else:
        state = "on"
    return jsonify(poolpumpState=state)
	
@app.route("/_tedpowernow")
def _tedpowernow():
	ted.reload()
	power = ted.get("Power","Total","PowerNow")
	return jsonify(tedPowerState=power)
    
# run the webserver on port 8083, requires sudo
if __name__ == "__main__":
    Pins.Init()
    app.run(host='0.0.0.0', port=8083, debug=True)