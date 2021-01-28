import os, hashlib
import dbinterface as db 

#Preforms a salted hash on password. Returns new hash and salt,
#   to be stored in database
def hashpass(password):
    salt = hashlib.sha256(os.urandom(60)
        ).hexdigest().encode('ascii')
    saltedpass = salt+(bytes(password.encode('ascii')))
    hashedpass = hashlib.sha256(saltedpass).hexdigest()

    return (salt.decode('ascii'), hashedpass)

#Preforms a salted hash on provided password. Uses salt stored in database for this user.
#   Compares the hash newly generated and the hash stored in database.
    #If ==, return True
    #If !=, return False
def checkpass(username, input):
    userData = db.query('users', 'salt, hash', 
        'WHERE username = \'{uName}\''.format(uName = username))

    if len(userData) != 1:
        return False
    userData=userData[0]

    saltedpass = userData[0].encode('ascii')+(input.encode('ascii'))
    hashedpass = hashlib.sha256(saltedpass).hexdigest()
    if hashedpass == userData[1]:
        return True
    return False


