from flask import Flask, render_template, Response, jsonify
import cv2
from gesture import process_frame, gesture, status
from pycaw.pycaw import AudioUtilities
import webbrowser
import threading

app = Flask(__name__)

cap = None
endpoint_volume = AudioUtilities.GetSpeakers().EndpointVolume

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

def generate_frames():
    global cap
    while True:
        if cap is None:
            continue

        success, frame = cap.read()

        if not success:
            break

        frame = process_frame(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start")
def start():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)
    return jsonify({"status": "started"})


@app.route("/stop")
def stop():
    global cap
    if cap:
        cap.release()
        cap=None
    return jsonify({"status": "stopped"})


@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/volume")
def volume():
    vol = int(endpoint_volume.GetMasterVolumeLevelScalar() * 100)
    return jsonify({"volume": vol})


@app.route("/gesture")
def get_gesture():
    return jsonify({
        "gesture": gesture,
        "status": status
    })


if __name__ == "__main__":
    threading.Timer(2.5, open_browser).start()
    app.run(debug=True)