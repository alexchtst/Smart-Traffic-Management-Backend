from flask import request
from random import randint
from models import crowddata

def cobaPredcit() -> list:
    try:
        retval = [
            {'date': '2025-03-04','val': randint(10, 20)},
            {'date': '2025-03-04','val': randint(10, 20)},
            {'date': '2025-03-04','val': randint(10, 20)},
            {'date': '2025-03-04','val': randint(10, 20)}
        ]
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
            
            predicted_data = cobaPredcit()
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
    
    # data reports bubub
    @socketio.on("data-reports")
    def datareport(data):
        try:
            socketio.emit("data-reports", {
                "data": data
            })
        except Exception as e:
            socketio.emit("data-reports", {
                "data": str(e)
            }, room=None)
            print(str(e))
    
    # data emergency bubub
    @socketio.on("emergency-data")
    def datareport(data):
        try:
            socketio.emit("emergency-data", {
                "data": data
            }, room=None)
        except Exception as e:
            socketio.emit("data-reports", {
                "data": str(e)
            })
            print(str(e))
    