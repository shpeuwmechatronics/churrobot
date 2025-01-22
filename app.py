import sys
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Made to run mock test on Windows and not run when on raspberry pi
if sys.platform.startswith('linux'):
    # Runs RPi.GPIO on raspberry pi if detected
    import RPi.GPIO as GPIO
else:
    # Mock RPi.GPIO on Windows
    from unittest import mock
    GPIO = mock.Mock()
    GPIO.getmode = mock.Mock(return_value=None)  # Mock getmode to return None (simulating a valid call)
    GPIO.setmode = mock.Mock()
    GPIO.setup = mock.Mock()
    GPIO.output = mock.Mock()

app = Flask(__name__)
socketio = SocketIO(app) # Dud potentially need to see what works for it

# Check if GPIO is available, otherwise mock it
if 'GPIO' in globals():
    GPIO.setmode(GPIO.BCM)  # To use GPIO pins for motor control

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    motor_pin = request.json.get('motor_pin')
    motor_state = request.json.get('motor_state')

    if 'GPIO' in globals():  # Only control the motor if GPIO is available
        if motor_state == 'ON':
            GPIO.output(motor_pin, GPIO.HIGH)
        else:
            GPIO.output(motor_pin, GPIO.LOW)

        return jsonify({"status": "success", "motor_state": motor_state})
    else:
        return jsonify({"status": "error", "message": "GPIO not available on this platform."})


if __name__ == '__main__':
    app.run(debug=False, port=5001)

