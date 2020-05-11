import sys
import json
import os, hashlib, datetime, base64
import dataBase as db
from flask import Flask
from flask import request, render_template, redirect, Response, jsonify, session, make_response, Blueprint

user = Blueprint('user', __name__, template_folder='templates')
socketio = None

@user.route('/check_id', methods = ['POST', 'GET'])
def checkID(id = None):
    if id == None:
        req = json.loads(request.data)
    else:
        req = id

    if 'userID' not in req:
        while True:
            id = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
            if len(db.query('users', 'id', 'WHERE id = \"{id}\"'.format(id = id))) == 0:
                break
        db.insert('users', '\"{id}\", \"{name}\", \'user\', 0, NULL, \"#ffffff\"'.format(id = id, name = req['newName'])) 
        return {'newID' : str(id)} 

    elif len(db.query('users', 'id', 'WHERE id = \"{id}\"'.format(id = req['userID']))) == 1:
        print("user.py ==> User " + req['userID'] + " is valid.")
        return {'isValid' : True}

    # print("user.py ==> User " + req['userID'] + " is invalid.")
    return {'isValid' : False}

@user.route('/control', methods = ['POST', 'GET'])
def controlCommand():
    req = json.loads(request.data)

    if req['pass'] == '3838abcdE!4949':
        if req['command'] == 'reload-all':
            socketio.emit('reload-device', {})
        elif req['command'] == 'message':
            socketio.emit('server-message', {'message' : req['message']})
    else:
        return 'Invalid Request'

@user.route('/user_data', methods = ['POST', 'GET'])
def getUserData():
    req = json.loads(request.data)
    
    if checkID(req)['isValid'] == False:
        return 'invalid_id'
    
    user = json.loads(
        db.tableToJSON(
            'users',
            db.query('users', args='WHERE id = \"{id}\"'.format(id = req['userID'])),
            ('account_id')
        )
    )
    user = user[0]

    return json.dumps(user)

@user.route('/update_user', methods = ['POST', 'GET'])
def setUserData():
    req = json.loads(request.data)

    if checkID(req)['isValid'] == False:
        return 'invalid_id'

    queryStr = None

    if 'color' in req and 'name' in req:
        queryStr = 'SET color = \"{color}\", name = \"{name}\" '.format(color = req['color'], name = req['name'])
    elif 'color' in req:
        queryStr = 'SET color = \"{color}\" '.format(color = req['color'])
    elif 'name' in req:
        queryStr = 'SET name = \"{name}\" '.format(name = req['name'])

    queryStr += 'WHERE id = \"{id}\"'.format(id = req['userID'])

    db.update('users', queryStr)

    return 'Changes saved'
