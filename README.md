# Picto
  - (1) The Idea
    - (1.1) Required Modules and Software
  - (2) **The Colo Update**
  - (3) Screenshots
## (1) A Pictochat (DS) like chat app (server/web-client)

I made this during the 2020 Corona Quarantine, as a personal challange during the boredom. Similar to Nintendo's Pictochat, you send drawn images as messages to chat rooms.

The server is both an API server and a web-page server, meaning that the client is used within the respective device's browser.

The client is designed for smartphones, as it requires a touch screen for drawing. *Of course, visiting the client from a PC will work with a mouse or trackpad, but the UI layout will only look right if you're in mobile layout mode in the browser web dev tools. *

The server can be run with `python colo.py`, opening the server to your local network. The server can be port forwarded to allow for global usage, too.
The client can be reached via the respective IP address (which depends on locality to server, if you're on the same network or not) at **port 5000**. 

*Example, on same machine visit localhost:5000.*

### (1.1) Required Modules and Software
### Server    
The server is written is python, using sqlite3 for the db. 

**Required**
  - Python 3
  - PyJWT *For auth tokens*
  - Flask *For web server*
  - flask_socketio *For sockets*
  
### Client
The client is web based. This means that as long as you have a semi modern broswer on a semi modern device, you should be fine.
  
## (2) Colo Update
I decided to repurpose this project for a class in 2020 Fall. I redesigned the security aspects, rebuilt the server entirerely, and added some nice features to the client. 

### Patch Notes
  - Client should work on iDevices now. Safari didn't make this easy, and I don't own an iPhone for testing, so millage may vary.
  - Accounts are now required! This makes the service more secure. 
    - **Keep in mind, though,** that accounts are stored on the device the server is running on, and are salted hashed to protect passwords. 
    - People are logged out after a certain period of inactivity, adjustable in server files. They are also logged out on server restarts, as the JWT auth tokens are only stored in volitile memory. *This is because I didn't want priavte tokens stored on disk.* 
    - Auth tokens are stored in the client browser's cookie jar. They will become **invalid** though after server restart, required the user to log in again. 
    - Auth tokens, once sent along with a request to the server and validated, are deleted, and the server will send a new token to replace the old one with it's reply to said request.
  - Added **captions**! When holding down on send button in client, a promt should appear for a caption. I think this is nice! 
  - Chat rooms have been overhauled.
    - The number of chat rooms, their names, and various attributes, are customizable in the chats dict at the top of the chat.py file.
    - Chat rooms have new attributes, such as a `persistantChats` var. Setting this to **true** will make server same save messages to disk, so that old messages can be revisited. Setting it to **false** will make all chats temporary.  

## (3) Screenshots

![s1](https://raw.githubusercontent.com/j-osephlong/Picto/master/screenshots/tia1735031959880705689.png)
![s2](https://raw.githubusercontent.com/j-osephlong/Picto/master/screenshots/tia6714663842891702589.png)
![s3](https://raw.githubusercontent.com/j-osephlong/Picto/master/screenshots/tia2191082126878982017.png)
![s4](https://raw.githubusercontent.com/j-osephlong/Picto/master/screenshots/tia4424003306902654980.png)
