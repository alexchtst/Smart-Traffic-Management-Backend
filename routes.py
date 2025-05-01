from flask import Blueprint, request, jsonify
from models import db, Region, GuardPost
from message_template import MESSAGE as message

routes = Blueprint('routes', __name__)

# ================== REGION ==================
@routes.route('/region', methods=['POST'])
def create_region():
    data = request.get_json()
    region = Region(
        name=data['name'],
        lat=data['lat'],
        long=data['long']
    )
    db.session.add(region)
    db.session.commit()
    return jsonify(region.todict()), 201

@routes.route('/region', methods=['GET'])
def get_regions():
    regions = Region.query.all()
    return jsonify([region.todict() for region in regions]), 200

@routes.route('/region/<int:id>', methods=['GET'])
def get_region(id):
    region = Region.query.get(id)
    if region is None:
        return jsonify(message[404]), 404
    
    return jsonify(region.todict()), 200

@routes.route('/region/<int:id>', methods=['PUT'])
def update_region(id):
    
    region = Region.query.get(id)
    
    if region is None:
        return jsonify(message[404]), 404
    
    data = request.get_json()
    region.name = data['name']
    region.lat = data['lat']
    region.long = data['long']
    db.session.commit()
    return jsonify(region.todict()), 200

@routes.route('/region/<int:id>', methods=['DELETE'])
def delete_region(id):
    region = Region.query.get(id)
    if region is None:
        return jsonify(message[404]), 404
    
    db.session.delete(region)
    db.session.commit()
    return jsonify(message[204]), 204
# ================== REGION ==================


# ================== GUARDPOST ==================
@routes.route('/guardpost', methods=['POST'])
def create_guardpost():
    data = request.get_json()
    guardpost = GuardPost(
        name=data['name'],
        lat=data['lat'],
        long=data['long'],
        reg_id=data['reg_id'],
    )
    db.session.add(guardpost)
    db.session.commit()
    return jsonify(guardpost.todict()), 201

@routes.route('/guardpost', methods=['GET'])
def get_guardposts():
    guardposts = GuardPost.query.all()
    return jsonify([guardpost.todict() for guardpost in guardposts]), 200

@routes.route('/guardpost/<int:id>', methods=['GET'])
def get_guardpost(id):
    guardpost = GuardPost.query.get(id)
    if guardpost is None:
        return jsonify(message[404]), 404
    
    return jsonify(guardpost.todict()), 200

@routes.route('/guardpost/<int:id>', methods=['PUT'])
def update_guardpost(id):
    
    guardpost = GuardPost.query.get(id)
    
    if guardpost is None:
        return jsonify(message[404]), 404
    
    data = request.get_json()
    guardpost.name = data['name']
    guardpost.lat = data['lat']
    guardpost.long = data['long']
    guardpost.reg_id = data['reg_id']
    db.session.commit()
    return jsonify(guardpost.todict()), 200

@routes.route('/guardpost/<int:id>', methods=['DELETE'])
def delete_guardpost(id):
    guardpost = GuardPost.query.get(id)
    if guardpost is None:
        return jsonify(message[404]), 404
    
    db.session.delete(guardpost)
    db.session.commit()
    return jsonify(message[204]), 204
# ================== GUARDPOST ==================