from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, jsonify
from flask.ext.socketio import SocketIO, emit
from threading import Thread
import Display
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
thread_TED = None
thread_DAE = None

@app.route("/_poolpump")
def _poolpump():
    state = request.args.get('state')
    if state=="on":
        Pins.PoolPumpon()
    else:
        Pins.PoolPumpoff()
    return jsonify(poolpumpState=state)

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
	
def TED_thread():
    from TED5000 import TED5000
    ted = TED5000()
    while True:
        #time.sleep(1)
        ted.reload()
        powernow = ted.get("Power","Total","PowerNow")/1000
        powernow = "%0.3f" % powernow
        voltagenow = ted.get("Voltage","Total","VoltageNow")/10
        voltagenow = "%0.1f" % voltagenow
        costnow = ted.get("Cost","Total","CostNow")/100
        costnow = "%0.2f" % costnow
        costtdy = ted.get("Cost","Total","CostTDY")/100
        costtdy = "%0.2f" % costtdy
        Display.ChangeDisplay(powernow, voltagenow, costnow, costtdy)
        data = dict(tedPowerState=powernow, tedVoltageState=voltagenow, tedCostState=costnow, tedCosttdyState=costtdy)
        #print "dict="+str(data)
        socketio.emit('TED', data)
		
def DAE_thread():
	from DAENetIP4 import DAENetIP4
	dae = DAENetIP4()
	while True:
		dae.reload()
		pooltemp = dae.get("AnalogInput4","Value")/7.64
		pooltemp = "%0.1f" % pooltemp
		data = dict(daePoolTempState=pooltemp)
		#print "dict="+str(data)
		socketio.emit('DAE', data)

@app.route('/')
def index():
    global thread_TED
    if thread_TED is None:
        thread_TED = Thread(target=TED_thread)
        thread_TED.start()
	global thread_DAE
    if thread_DAE is None:
        thread_DAE = Thread(target=DAE_thread)
        thread_DAE.start()
        
    return render_template('index.html')

@socketio.on('pool_pump')
def pool_pump(data):
    state = data["state"]
    if state=="on":
        Pins.PoolPumpOn()
    else:
        Pins.PoolPumpOff()
    emit("pool_pump_status", {"state": state}, broadcast=True)
	
@socketio.on('pond_pump')
def pond_pump(data):
    state = data["state"]
    if state=="on":
        Pins.PondPumpOn()
    else:
        Pins.PondPumpOff()
	emit("pond_pump_status", {"state": state}, broadcast=True)

@socketio.on('my broadcast event')
def test_broadcast_message(message):
    emit('my response',
         {'data': message['data'], 'count': 10},
         broadcast=True)
    
# run the webserver, requires sudo
if __name__ == "__main__":
    Pins.Init()
    socketio.run(app, host="0.0.0.0", port=PORT)
