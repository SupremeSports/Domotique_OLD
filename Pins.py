import RPi.GPIO as GPIO

# BCM to WiringPi pin numbers
PoolPumpOut = 13 # LED pin
P1 = 18 # Button pin

def Init():
    GPIO.setwarnings(False) # suppress GPIO used message
    GPIO.setmode(GPIO.BCM) # use BCM pin numbers
    GPIO.setup(PoolPumpOut, GPIO.OUT) # set LED pin as output
    # set button pin as input
    # also use internal pull-up so we don't need external resistor
    GPIO.setup(P1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def PoolPumpon():
    GPIO.output(PoolPumpOut, GPIO.HIGH)

def PoolPumpoff():
    GPIO.output(PoolPumpOut, GPIO.LOW)

def SetLED(state):
    if state:
        LEDon()
    else:
        LEDoff()

# the "not" is used to reverse the state of the input
# when pull-up is used, 1 is returned when the button is not pressed
def ReadButton():
    if not GPIO.input(P1):
        return True
    else:
        return False
		
def ReadPoolPump():
    #GPIO.setup(PoolPumpOut, GPIO.IN)
    if not GPIO.input(PoolPumpOut):
        return True
    else:
        return False

# if not used as a module (standalone), run this test program 
if __name__ == "__main__":
    Init()
    try:
        while(True):
            SetLED(ReadButton())
    except:
        #clean exit on CTRL-C
        GPIO.cleanup()
        quit()