import sys
import json
import os, hashlib, datetime, base64

from flask import Flask
from flask import request, render_template, redirect, Response, jsonify, session, make_response, send_from_directory
from flask_socketio import SocketIO

import dataBase as db, user, chat

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fwordsecret'
socketio = SocketIO(app)

app.register_blueprint(user.user)
app.register_blueprint(chat.chat)

@app.route("/draw_test2", methods=['POST', 'GET'])
def drawTest2():
    resp = make_response(render_template("ui.html"))
    return resp

@app.route("/chat", methods=['POST', 'GET'])
def serverChat():
    resp = make_response(render_template("chat.html"))
    return resp
        
@app.route("/")
def serveHomePage():
    # id = user.checkID(request.cookies)
    # resp = make_response(render_template("test.html"))
    # resp.set_cookie('userID', str(id), expires = datetime.datetime.max)
    
    return render_template("index.html")

@app.route('/sw.js')
def sw():
    return app.send_static_file('sw.js')

if __name__ == "__main__":
    db.initDB()
    chat.socketio = socketio
    user.socketio = socketio

    app.secret_key = 'fuck'
    socketio.run(app, host='0.0.0.0', port = 5000, debug=False)#192.168.2.21 // ssl_context='adhoc'
    