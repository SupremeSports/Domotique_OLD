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

# return index page when IP address of RPi is typed in the browser
@app.route("/")
def Index():
    return render_template("index.html", uptime=GetUptime())

# ajax GET call this function to set led state
# depeding on the GET parameter sent
@app.route("/_poolpump")
def _poolpump():
    state = request.args.get('state')
    if state=="on":
        Pins.PoolPumpon()
    else:
        Pins.PoolPumpoff()
    return ""
	
def _pondpump():
    state = request.args.get('state')
    if state=="on":
        Pins.LEDon()
    else:
        Pins.LEDoff()
    return ""

# ajax GET call this function periodically to read button state
# the state is sent back as json data
@app.route("/_button")
def _button():
    if Pins.ReadButton():
        state = "pressed"
    else:
        state = "not pressed"
    return jsonify(buttonState=state)

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
	
def GetUptime():
    # get uptime from the linux terminal command
    from subprocess import check_output
    output = check_output(["uptime"])
    # return only uptime info
    uptime = output[output.find("up"):output.find("user")-5]
    return uptime
    
# run the webserver on port 8083, requires sudo
if __name__ == "__main__":
    Pins.Init()
    app.run(host='0.0.0.0', port=8083, debug=True)