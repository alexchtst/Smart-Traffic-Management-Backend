from flask import request
from models import crowddata
import numpy as np
from datetime import datetime
from ultralytics import YOLO
import base64
import cv2
import joblib
import numpy as np

# Load pipeline
lstm_pipeline = joblib.load("model/rf_pipeline.joblib")

model = YOLO("model/ambulance5mar.pt")

def PredSequence(data) -> list:
    try:
        array_input = [i['val'] for i in data]
        time = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
        array_input = np.array(array_input).reshape(1, -1)
        prediction_value = int(lstm_pipeline.predict(array_input)[0])
        retval = []
        for i in data:
            retval.append({'date': i['date'], 'val': i['val']})
        retval.append({'date': time, 'val': prediction_value})
        return retval
    except Exception as e:
        print("error happened", str(e))
        return {
            "data": [{
                'date': '2025-03-04',
                'val': -1
            }]
        }

def data_event(socketio):
    @socketio.on("crowd-realtime")
    def realtime(data):
        sender_id = request.sid
        try:
            crowddata.insert_one(data['data'][0])
            data_db = crowddata.find({}, {'_id': 0})
            crowdData = [i for i in data_db]
            
            print(len(crowdData), "has been sent")
            
            socketio.emit("crowd-realtime", {
                "data": crowdData[-25:]
            })
            
            predicted_data = PredSequence(crowdData[-4:])
            socketio.emit("predictive-realtime", {
                "data": predicted_data
            })
            
        except Exception as e:
            socketio.emit("crowd-realtime", {
                "data": str(e)
            }, room = None)
            
            socketio.emit("predictive-realtime", {
                "data": str(e)
            }, room=None)
            
            print('error happened', str(e))

    @socketio.on('video_frame')
    def handle_video_frame(data):
        try:
            frame_data = data['image']
            encoded_data = frame_data.split(',')[1]
            img_bytes = base64.b64decode(encoded_data)
            img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)

            results = model(img)

            detections = []
            for box in results[0].boxes:
                detections.append({
                    'class': int(box.cls[0]),
                    'confidence': float(box.conf[0]),
                    'bbox': [float(x) for x in box.xyxy[0]]
                })

            # Anotasi opsional
            annotated = results[0].plot()
            _, buffer = cv2.imencode('.jpg', annotated)
            annotated_b64 = base64.b64encode(buffer).decode('utf-8')

            # Kirim hasil deteksi ke klien yang memicu event
            socketio.emit(
                'detection_result',
                {
                    'detections': detections,
                    'annotated_frame': 'data:image/jpeg;base64,' + annotated_b64
                },
                to=request.sid  # Kirim hanya ke klien yang memicu event
            )

        except Exception as e:
            print(f"Error dalam frame processing: {str(e)}")
        