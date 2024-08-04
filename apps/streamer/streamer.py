# import the necessary packages
from flask import Flask, request, jsonify, render_template_string, Response
from cv_recon import cv_tools
from cv_recon.picam import PiCam
from time import sleep
from datetime import datetime
import cv2 as cv
import threading
import socket
import os

class Streamer():
    def __init__(self, app_name='default', save_rate_s = 10, record = False, res=(320, 240), fps=24, port=3141):
        self.VIDEO_PORT = port
        self.HOST = self.get_local_ip()

        self.save_rate_s = save_rate_s
        self.record = record

        self.frame = []
        self.res = res
        self.fps = fps
        self.camera = PiCam(res, fps)

        self.app = Flask(app_name)
        self.setup_routes()

        self.set_up_record()

    @staticmethod
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip

    def info(self):
        print(f"[+] Resolution: {self.res}")
        print(f"[+] Fps: {self.fps}")
        print(f"[+] Record: {self.record}")
        print(f"[+] Save rate: {self.save_rate_s}s")
        print(f"[+] Save path: {self.save_path}")

    def set_up_record(self):
        self.start_app_datetime = datetime.now()
        if self.record:
            self.save_path = f'./{self.start_app_datetime:%Y-%m-%d-%H-%M-%S}'
            os.makedirs(self.save_path, exist_ok=True)
            print(f"[+] Created: {self.save_path}")
        else:
            self.save_path = ''

    def get_frames(self):
        last_datetime = datetime.now()
        #global update
        while True:
            #if update:
            sleep(0.1)
            try:
                ret, buffer = cv.imencode('.jpg', self.frame)
            except:
                continue

            if self.record:
                current_datetime = datetime.now()
                time_diff = (current_datetime - last_datetime).seconds
                if time_diff >= self.save_rate_s:
                    file_path = f"{self.save_path}/{current_datetime:%Y-%m-%d-%H-%M-%S}.jpg"
                    print(file_path)
                    cv.imwrite(file_path, self.frame)
                    last_datetime = datetime.now()

            self.frame = buffer.tobytes()
            yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')

    def setup_routes(self):
        @self.app.route('/')
        def index():
            print("created /")
            return render_template_string('''<html>
            <head>
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/p5@1.3.1/lib/p5.js"></script>
                <title>Stream</title>
            </head>
            <body>
                <h1>PiCamStream</h1>
                <button id="start-button", style="width: 120px; height: 35px; margin: 5px">Start</button>
                <button id="stop-button", style="width: 120px; height: 35px; margin: 5px">Stop</button>
                <br><br>
                <img src="/stream" width="80%">
            </body>
            </html>

            <script>
            $(document).ready(function(){
                $('#start-button').click(function(){
                    let actionData = { action: "start" };

                    $.ajax({
                        url: '/action',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify(actionData),
                        dataType: 'json',
                        success: function(data) {
                            console.log('Success:', data);
                            toggleState();
                        },
                        error: function(error) {
                            console.error('Error:', error);
                        }
                    });
                });
            });

            $(document).ready(function(){
                $('#stop-button').click(function(){
                    let actionData = { action: "stop" };

                    $.ajax({
                        url: '/action',
                        type: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify(actionData),
                        dataType: 'json',
                        success: function(data) {
                            console.log('Success:', data);
                            toggleState();
                        },
                        error: function(error) {
                            console.error('Error:', error);
                        }
                    });
                });
            });
            </script>
            ''')

        @self.app.route('/stream')
        def stream():
            return Response(self.get_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/action', methods=['POST'])
        def action():
            data = request.json

            if data['action'] == 'start':
                print("[+] Start pressed")
                if self.record:
                    print("[!] Already recording")
                else:
                    self.record = True
                    self.set_up_record()
            elif data['action'] == 'stop':
                print("[+] Stop pressed")
                self.record = False

            return jsonify({"status": "success"})

    def start_flask(self):
        self.app.run(debug=False, host=self.HOST, port=self.VIDEO_PORT)

    def start_cam(self):
        self.camera.videoCapture()

        # allow the camera to warmup
        sleep(2.0)
        # capture frames from the camera
        while True:
            sleep(0.2)
            self.frame = self.camera.current_frame
            # if not update: update = True
            if cv.waitKey(1) & 0xFF == ord("q"):
                break
        # update = False
        cv.destroyAllWindows()

if __name__ == '__main__':
    s = Streamer(app_name = __name__, record = True)
    s.info()
    t_flask = threading.Thread(target=s.start_flask, args=())
    t_flask.start()
    s.start_cam()
