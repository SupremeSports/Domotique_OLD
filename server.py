from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, jsonify
from flask.ext.socketio import SocketIO, emit
from XML import SimpleParser
from threading import Thread
#import Display
import template
import Pins
import time
import sys


try:
    PORT = int(sys.argv[1])
except:     
    PORT = 8083

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

pool_pump = template.Button("pool_pump", "Pompe Piscine")
pond_pump = template.Button("pond_pump", "Pompe Etang")
thermopompe = template.Button("thermopompe", "Thermopompe Piscine")

socketio.on("pool_pump")(pool_pump.event)
socketio.on("pond_pump")(pond_pump.event)
socketio.on("thermopompe")(thermopompe.event)

@app.route('/')
def index():
    runThreads()
    browser = request.user_agent.browser 
    if browser == "chrome":
        template.ChromeBrowser()
    else:
        template.OtherBrowsers()
    return render_template('index.html', **template.context)

def TED_thread():
    ted = SimpleParser()
    while True:
        ted.reload()
        powernow = ted.get("Power","Total","PowerNow")/1000
        powernow = "%0.3f" % powernow
        voltagenow = ted.get("Voltage","Total","VoltageNow")/10
        voltagenow = "%0.1f" % voltagenow
        costnow = ted.get("Cost","Total","CostNow")/100
        costnow = "%0.2f" % costnow
        costtdy = ted.get("Cost","Total","CostTDY")/100
        costtdy = "%0.2f" % costtdy
        #Display.ChangeDisplay(powernow, voltagenow, costnow, costtdy)
        data = dict(tedPowerState=powernow, tedVoltageState=voltagenow, tedCostState=costnow, tedCosttdyState=costtdy)
        #print "dict="+str(data)
        socketio.emit('TED', data)
		
def DAE_thread():
	dae = SimpleParser(url="http://supremesports.ddns.net:8082/current_state.xml?pw=abcd1234")
	while True:
		dae.reload()
		pooltemp = dae.get("AnalogInput4","Value")/7.64
		pooltemp = "%0.1f" % pooltemp
		data = dict(daePoolTempState=pooltemp)
		#print "dict="+str(data)
		socketio.emit('DAE', data)

thread_TED = None
thread_DAE = None
def runThreads():
    global thread_TED
    if thread_TED is None:
        thread_TED = Thread(target=TED_thread)
        thread_TED.start()
	global thread_DAE
    if thread_DAE is None:
        thread_DAE = Thread(target=DAE_thread)
        thread_DAE.start()

# run the webserver, requires sudo
if __name__ == "__main__":
    Pins.Init()
    socketio.run(app, host="0.0.0.0", port=PORT)
