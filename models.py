from flask_sqlalchemy import SQLAlchemy
import pymongo

mongo_client = pymongo.MongoClient("mongodb+srv://acinatra:nflRVQ8nDedqP2bw@cluster0.upuf4.mongodb.net/?retryWrites=true&w=majority")
mongodb = mongo_client["Cluster0"]

crowddata = mongodb["testcrowddata"]

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    passkey = db.Column(db.String(128), nullable=False)
    
    def todict(self):
        return {
            'id': self.id,
            'email': self.email,
            'passkey': self.passkey
        }
        
    def check_password(self, password):
        return self.passkey == password

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    long = db.Column(db.Integer, nullable=False)
    guard_post = db.relationship('GuardPost')
    
    def todict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': [self.lat, self.long],
            'lat': self.lat,
            'long': self.long
        }

class GuardPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    long = db.Column(db.Integer, nullable=False)
    
    region_id = db.Column(
        db.Integer,
        db.ForeignKey('region.id', ondelete='CASCADE'),
        nullable=False
    )
    
    def todict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': [self.lat, self.long],
            'lat': self.lat,
            'long': self.long
        }

class Crowded(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    time_detect = db.Column(db.String(255), nullable=False)
    vehicle_number = db.Column(db.Integer, nullable=False)
    
    def todict(self):
        return {
            'id': self.id,
            'time_detect': self.time_detect,
            'vehicle_number': self.vehicle_number
        }
