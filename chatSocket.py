#THIS FILE IS A BIT ANNOYING BUT IT'S NECESSARY

#This module exists to separate the socketIO object from 
#   the main python file.
#Doing this allows me to reference and add to the socketIO module from other 
#   modules (like Chat.py) rather than build all of the socket in the main
#   python file, which would be really ugly.

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)