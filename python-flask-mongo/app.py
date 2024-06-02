import os
from flask import Flask, request, jsonify
from pymongo import MongoClient

application = Flask(__name__)

MONGO_URI = 'mongodb://' + os.environ['MONGO_PI_USERNAME'] + ':' + os.environ['MONGO_PI_PASSWORD'] + '@' + os.environ['MONGO_HOSTNAME'] + ':' + os.environ['MONGO_PORT']

client = MongoClient(MONGO_URI)
db = client[os.environ['MONGO_PI_DATABASE']]

@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )

@application.route('/telegram')
def getTelegramLogs():
    _telegram = db.telegram.find()

    item = {}
    data = []
    for telegram in _telegram:
        item = {
            'id': str(telegram['_id']),
            'telegram': telegram['telegram']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@application.route('/telegram', methods=['POST'])
def putTelegramLogs():
    data = request.get_json(force=True)
    item = {
        'telegram': data['telegram']
    }
    db.telegram.insert_one(item)

    return jsonify(
        status=True,
        message='telegram saved successfully!'
    ), 201

@application.route('/lifx')
def getLifxLogs():
    _lifx = db.lifx.find()

    item = {}
    data = []
    for lifx in _lifx:
        item = {
            'id': str(lifx['_id']),
            'lifx': lifx['lifx']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )

@application.route('/lifx', methods=['POST'])
def putLifxLogs():
    data = request.get_json(force=True)
    item = {
        'lifx': data['lifx']
    }
    db.lifx.insert_one(item)

    return jsonify(
        status=True,
        message='lifx saved successfully!'
    ), 201



if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
