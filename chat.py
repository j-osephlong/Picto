import user, dbinterface as db
from user import tokenAuth
from chatSocket import sio
from flask import Flask
from flask import request, render_template, redirect, Response, jsonify, session, make_response, Blueprint
from flask_socketio import SocketIO, join_room, leave_room

from datetime import datetime
import json

chat = Blueprint('chat', __name__, template_folder='templates')

#data structure defining chat rooms
    #N refers to number of messages in the room
    #PersistantChats determines if messages should be saved to server and request by client on join 
chats = {
            0 : {
                'name': 'Main Chat',
                'creator': 'server',
                'activeSince': datetime.now(),
                'users': [],
                'persistantChats': True,
                'N':0,
                'id': 0
            },
            -1 : {
                'name': 'Testing Room',
                'creator': 'server',
                'activeSince': datetime.now(),
                'users': [],
                'persistantChats': False,
                'N':0,
                'id':-1
            }  
        }

#retrieve number of messages in a group chat from the db
def initChats():
    for chat in chats:
        N = int(db.query('msgs', 'COUNT(*)', 'WHERE chatID = ' + str(chat))[0][0])
        chats[chat]['N'] = N

#NOT IMPLIMENTED
@chat.route('/chat/makeChat', methods=['POST'])
def makeChat():
    pass

#socket event called when user socket 'joins' a chatroom
@sio.on('join')
def joinChat(data):
    #verify user token
    newToken = tokenAuth(data['userName'], data['token'])
    #if bad token, send bad token error to client, 401
    if not newToken:
        print('badToken')
        return {'error':'invalid-token'}, 401

    #if user attempts to join a non existent chat, return 400
    if int(data['chatID']) not in chats:
        print('badChat')
        return {'error':'invalid-chatID'}, 400 

    #log the user, user->socket ID, and the chatID
    #this log is user to clean up when a user leaves a room
    user.userSockets[request.sid] = (data['userName'], int(data['chatID']))

    #call to socketIO lib
    join_room(int(data['chatID']))
    
    #log username in chatRoom data struct
    if data['userName'] not in chats[int(data['chatID'])]['users']:
        chats[int(data['chatID'])]['users'].append(data['userName'])

    print(str(data['chatID'])+" - "+str(chats[int(data['chatID'])]['users']))
 
    #emit a user joined event
    sio.emit('userJoined', {'username': data['userName']}, room = int(data['chatID']))
    return {'chatID':data['chatID'], 'newToken':newToken}

#return specific chat room data structure to client
@chat.route('/chat/chatInfo', methods=['GET'])
def getChatInfo():
    data = request.json
    return chats[int(data['chatID'])]

#return all chat rooms data structure to client
@chat.route('/chat/listChats', methods=['GET'])
def listChats():
    #token not required - public info
    return chats

#handle new msg from a client
@chat.route('/chat/send', methods=['POST'])
def newMsg():
    data = json.loads(request.data)

    #verify that chat room exists
    if int(data['chatID']) not in chats:
        return {'error':'invalid-chatID'}, 400

    #verify user token
    newToken = tokenAuth(data['userName'], data['token'])
    if newToken == False:
        return {'error': 'invalid-token'}, 401

    #increment number of messages in chat room
    chats[int(data['chatID'])]['N']+=1
    
    #send socket event to all chat rooms in a particular chat room
    sio.emit('newMessage', {
        'imgData':data['img'],
        'userName':data['userName'],
        'msgID':int(chats[int(data['chatID'])]['N']),
        'caption': data['caption']
    }, room=int(data['chatID']))

    #if chat room has persistant chats enabled, save message to db
    if chats[int(data['chatID'])]['persistantChats']:
        print('saving msg in chat' + str(data['chatID']))
        db.insert('msgs', (
            str(data['chatID']),
            str(chats[int(data['chatID'])]['N']),
            "\'"+data['userName']+"\'",
            "\'"+str(datetime.now())+"\'",
            "\'"+data['img']+"\'",
            "\'"+data['caption']+"\'" if (data['caption'] != None) else "'None'"
        ))

    return {'newToken': newToken}

#send batches of previous messages to user, based off of offset and # to send
#used when client joins or scolls past saved messages
@chat.route('/chat/fetch', methods=['POST'])
def sendMsgsBulk():
    data = json.loads(request.data)

    #verify chat room exists
    if int(data['chatID']) not in chats:
        return {'error':'invalid-chatID'}, 400

    #verify user token
    newToken = tokenAuth(data['userName'], data['token'])
    if newToken == False:
        return {'error': 'invalid-token'}, 401

    offset = data['offset']
    n = data['n']
    chatID = data['chatID']

    #get requested batch from db, and then convert matrix from db into JSON
    messages = db.toJSON('msgs', 
        db.query('msgs', args='WHERE chatID = {c} ORDER BY msgID DESC LIMIT {o}, {n}'.format(c = chatID, o = offset, n = n)),
        ('sentAt', 'chatID'))

    return {'newToken':newToken, 'msgs': messages}

#automatic event when socket loses connected to user socket, user disconnected
#cleans up user/chat data
@sio.on('disconnect')
def disconnect():
    #find user sid match
    username = None
    chatID = None
    sid = None
    for sid in user.userSockets:
        if sid == request.sid:
            sid = request.sid
            break
    
    #if no user->sid match, quit
    if sid == None:
        print("socket " + str(request.sid) + " disconnected")
        return;

    #if match, get their username and join chatRoom id 
    username = user.userSockets[sid][0]
    chatID = user.userSockets[sid][1]
    #delete user->sid record
    del user.userSockets[sid]
    #force sid to leave chatRoom
    leave_room(chatID)

    #send userLeft to all clients in room
    sio.emit('userLeft', {'username': username}, room = chatID)
    # chats[chatID]['users'].remove(username) <- weird

    print("user " + str(username) + " left chat " + str(chatID))