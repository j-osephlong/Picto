from flask import render_template
from chat import initChats
from chatSocket import app, sio
import user, chat, dbinterface as db, sys


# Connect other server modules (Chat.py, User.py)
app.register_blueprint(user.user)
app.register_blueprint(chat.chat)

#Following two methods return their respective HTML documents
@app.route('/chat')
def serverChat():
    return render_template("chat.html")

@app.route('/')
def serverHome():
    return render_template("index.html")

#This is basically the "main()" or entry point of the server
if __name__ == "__main__":
    db.initDB() # <- Initialize the sqlite database
    initChats() # <- Initialize the chat rooms from the database

    #Entry point for the socket server and HTML server
    sio.run(app, host='0.0.0.0', port = 5000, debug=True) 