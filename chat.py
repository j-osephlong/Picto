import sys
import json
import os, hashlib, datetime, base64
import dataBase as db
from flask import Flask
from flask import request, render_template, redirect, Response, jsonify, session, make_response, Blueprint

chat = Blueprint('chat', __name__, template_folder='templates')

socketio = None

@chat.route('/send_message', methods = ['POST'])
def recieveMessage():
    req = json.loads(request.data)
    file = str(req['image'])
    print(file[0:100])

    messageID = db.query('messages', 'messageID', 'ORDER BY messageID DESC')[0][0] + 1
    filePath = "messages/bucket"+str(req['bucket'])+"/"+"message"+str(messageID)+".png"
    
    base64.b64decode(file[file.index(',')+1:])
    image = open (filePath, "wb")
    image.write(base64.b64decode(file[file.index(',')+1:]))

    time = int(datetime.datetime.now().strftime('%Y%m%d%H%M'))
    db.insert('messages', '{mID}, \"{uID}\", {b}, {t}, \"{f}\"'.format(
        mID = messageID, uID = req['userID'], b = req['bucket'], t = time, f = filePath 
    ))
    image.close()

    socketio.emit('newMessage', {
        'id' : messageID,
        'userName' : db.query('users', 'name', 'WHERE id = \"{id}\"'.format(id = req['userID']))[0][0],
        'image': file[file.index(',')+1:],
        'bucket': req['bucket']
    })

    return 'Success!'

@chat.route('/get_messages', methods = ['POST'])
def getXRecent():
    req = json.loads(request.data)
    offset = req['offset']
    n = req['n']
    bucket = None

    if 'bucket' in req:
        bucket = req['bucket']
    else:
        bucket = 0

    messages = db.tableToJSON('messages', 
        db.query('messages', args='WHERE bucket = {b} ORDER BY messageID DESC LIMIT {o}, {n}'.format(b = bucket, o = offset, n = n)),
        ('bucket', 'time'))
        
    if len(messages) == 0:
        return 'no_messages' #No messages to return

    m = json.loads(messages)
    for message in m:
        message['userName'] = db.query('users', 'name', 'WHERE id = \"{u}\"'.format(u = message['userID']))[0][0]
        del message['userID']
        file = open(message['filename'], 'rb')
        message['image'] = str(base64.b64encode(file.read()))[2:-1] #[2:] to get rid of "b'"" prefix
        file.close()
        del message['filename']

    return json.dumps(m)