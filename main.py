from enum import Enum
from time import sleep
from flask import Flask, render_template
from flask.globals import request
from gpiozero import LED
import atexit

# State Machine ---
class Status(Enum):
    Idle=0
    Busy=1
    Meeting=2

currentStatus = Status.Idle

# Initialize LEDs only once
idleLED = None
busyLED = None
meetingLED = None

def init_gpios():
    global idleLED, busyLED, meetingLED
    if idleLED is None:
        # Physical pin mapping to BCM GPIO numbers:
        # Physical pin 3 = GPIO2 (BCM)
        # Physical pin 5 = GPIO3 (BCM)
        # Physical pin 7 = GPIO4 (BCM)
        idleLED = LED(2)      # Physical pin 3
        busyLED = LED(3)      # Physical pin 5
        meetingLED = LED(4)   # Physical pin 7
        setStatus(Status.Idle)

def cleanup_gpios():
    if idleLED:
        idleLED.close()
    if busyLED:
        busyLED.close()
    if meetingLED:
        meetingLED.close()

atexit.register(cleanup_gpios)

def setStatus(status: Status):
    global currentStatus
    idleLED.off()
    busyLED.off()
    meetingLED.off()
    if status == Status.Idle:
        idleLED.on()
    elif status == Status.Busy:
        busyLED.on()
    elif status == Status.Meeting:
        meetingLED.on()
    currentStatus = status

# Flask Setup ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.get('/api/status')
def status():
    return {
        "status": int(currentStatus.value)
    }

@app.post('/api/status')
def statusPost():
    global currentStatus
    foundStatus = request.form.get("status")  # Changed to .get() for safety
    if not foundStatus:
        print('no found status')
        return {
            "status": int(currentStatus.value)
        }
    statusFormatted = int(foundStatus)
    print(statusFormatted, type(statusFormatted))
    if statusFormatted not in [0, 1, 2]:
        print('bad formatting - invalid status value')
        return {
            "status": int(currentStatus.value)
        }
    setStatus(Status(statusFormatted))
    return {
        "status": int(currentStatus.value)
    }

if __name__ == "__main__":
    init_gpios()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
