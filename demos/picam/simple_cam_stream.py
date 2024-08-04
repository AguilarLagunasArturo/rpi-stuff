# import the necessary packages
from flask import Flask, render_template_string, Response
from cv_recon import cv_tools
from time import sleep
import numpy as np
import cv2 as cv
import threading
import socket

''' Video Streaming '''
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

HOST = get_local_ip()
VIDEO_PORT = 6282

frame = []
# update = False
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''<html>
    <head>
        <title>Stream</title>
    </head>
    <body>
        <img src="{{ url_for('stream') }}" width="100%">
    </body>
    </html>''')

@app.route('/stream')
def stream():
    return Response(get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_frames():
    global frame
    #global update
    while True:
        #if update:
        sleep(0.5)
        try:
            ret, buffer = cv.imencode('.jpg', frame)
        except:
            continue
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def start_flask():
    app.run(debug=False, host=HOST, port=VIDEO_PORT)

t_flask = threading.Thread(target=start_flask, args=())
t_flask.start()

''' Video Recording '''
# initialize the camera
cam = cv.VideoCapture(0)
# allow the camera to warmup
sleep(2.0)
# capture frames from the camera
while True:
    sleep(0.5)
    _, frame = cam.read()
    # cv.imshow('grid', frame)
    # if not update: update = True
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
cv.destroyAllWindows()
