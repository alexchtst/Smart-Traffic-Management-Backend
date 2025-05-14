from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO


from config import Config as C
from models import db
from routes import routes as api
from auth import routes as auth, jwt
from datafeed import data_event

from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

from seed_data import Seedguardpost


app = Flask(__name__)
app.config.from_object(C)
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# foreign key activation
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

with app.app_context():
    print("create tables")
    db.create_all()
    print("seed crowded and post data")
    Seedguardpost(app)
    
app.register_blueprint(auth)
app.register_blueprint(api)

data_event(socketio=socketio)

@app.route('/')
def index():
    return "Selamat datang pengunjung, awokwok"

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)