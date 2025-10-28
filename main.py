from flask import Flask, render_template
from enum import Enum

from flask.globals import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

class Status(Enum):
    Idle=0
    Busy=1
    Meeting=2

currentStatus = Status.Idle

@app.get('/api/status')
def status():
    return {
        "status": int(currentStatus.value)
    }

@app.post('/api/status')
def statusPost():
    global currentStatus
    foundStatus = request.form["status"]
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

    currentStatus = Status(statusFormatted)

    return {
        "status": int(currentStatus.value)
    }

if __name__ == "__main__":
    app.run(debug=True)
