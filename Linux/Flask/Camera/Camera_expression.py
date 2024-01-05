from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace

from queue import Queue
from flask_cors import CORS

is_camera_running = False
send_face = ""
face_list = []

def generate_expression():
    global is_camera_running
    global send_face

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while is_camera_running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        try:
            response = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            dominant_emotion = response[0]["dominant_emotion"]

        
            output = dominant_emotion
            simle_level = response[0]["emotion"][dominant_emotion]

            if dominant_emotion == "happy":
                if simle_level >90:
                    output= "bigsmile"
            
                else:
                    output= "smile"
            elif dominant_emotion in [ "disgust",  "fear"  ]:
                output = "neutral"

            if output is not send_face:    
                print(output)
                send_face = output
                yield f"data: {output}\n\n"
               
        except Exception as e:
            print(f"Error analyzing frame: {e}")

    cap.release()


def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    global is_camera_running
    while is_camera_running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()


app = Flask(__name__)
app.debug = False
CORS(app)
queue = Queue()

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route for starting the video stream
@app.route('/expression_start')
def video_start():
    global is_camera_running
    is_camera_running = True
    return Response(generate_expression(), mimetype='text/event-stream')

@app.route("/camera")
def startCamera():
    global is_camera_running
    is_camera_running = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stop")
def stopCamera():
    global is_camera_running
    is_camera_running = False
    return Response("is_camera_running",is_camera_running)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=1500)
    # app.run(debug=True, port=1500)
