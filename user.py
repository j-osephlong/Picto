from flask import Flask
from flask import request, render_template, redirect, Response, jsonify, session, make_response, Blueprint
import jwt, json, userhash, hashlib, os, datetime, codecs
import dbinterface as db

#Define Flask blueprint, allows for modular server
user = Blueprint('user', __name__, template_folder='templates')

#This server uses JWT tokens to verify users identity.
#   To make tokens secure, we use a 'secret'. This line creates that secret.  
tokenSecret = str(hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii'))

#All tokens are stored in this dictionary (username -> token)
tokens = {}

#Socket ID's are stored in this dict, mapping to a 2-tuple of (username, chatID)
#   Used to handle socket disconnections
userSockets = {}

@user.route('/user/register', methods=['POST'])
def createUser():
    #get JSON of request
    data = json.loads(request.data)

    #check if username free
    if len(db.query('users', 'username', 
        'WHERE username = \'{uName}\''.format(uName = data['userName']))) > 0:
        return {'error' : 'name_claimed'}, 400
    
    #if username free, hash it and store the hash + salt
    salt, hash = userhash.hashpass(data['password'])
    db.insert('users', ("\'"+data['userName']+"\'", "\'"+salt+"\'", "\'"+hash+"\'"))
    
    #send back a new token
    userToken = createToken(data['userName'])
    tokens[data['userName']] = userToken
    return {'token' : userToken}
    
#Method creates a new token with a username payload, a half-hour expiry,
#   and the secret  
def createToken(username):
    return jwt.encode({'userName': username, 'exp' : datetime.datetime.utcnow()+datetime.timedelta(minutes = 30)}
        , tokenSecret, algorithm='HS256').hex()

#Method used for login. Returns a token on success
@user.route('/user/auth', methods=['POST'])
def userAuth():
    data = json.loads(request.data)

    #check that user exists in database
    if len(db.query('users', 'username', 
        'WHERE username = \'{uName}\''.format(uName = data['userName'])))  != 1:
        return {'error' : "invalid-username"}, 401
    
    #if user exists, check that the password, when hashed, matches the stored
    #   user password hash. If so, send token
    if userhash.checkpass(data['userName'], data['password']):
        userToken = createToken(data['userName'])
        tokens[data['userName']] = userToken
        return {'token' : userToken}
    else: 
        return {'error' : 'invalid-pass'}, 401

#Method used by any request handler that needs to verify a token.
    #If valid, method destroys old token and returns a new one.
    #If invalid, returns false.
def tokenAuth(username, token):
    user = None
    try:
        user = jwt.decode(codecs.decode(token, "hex"), tokenSecret, algorithms=['HS256'])['userName']
    except Exception as E:
        print(str(E))
        return False

    if user != username:
        return False

    if user in tokens:
        if tokens[user] != token:
            return False
    
    newToken = createToken(username)
    tokens[user] = newToken
    return newToken

#Method used by client to verify that token still valid. 
    #Returns new token if valid.
@user.route('/user/me', methods=['POST'])
def getSelf():
    data = json.loads(request.data)
    newToken = tokenAuth(data['userName'], data['token'])
    if newToken == False:
        return {'error': 'invalid-token'}, 401
    return {'Yay!':True, 'newToken':newToken}
