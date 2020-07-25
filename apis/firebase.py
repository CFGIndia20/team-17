import pyrebase

firebaseconfig = {
    "apiKey": "AIzaSyDgFX_9PtztpFf-d71uEcBr43SWth-EVcs",
    "authDomain": "janagraha-cce3a.firebaseapp.com",
    "databaseURL": "https://janagraha-cce3a.firebaseio.com",
    "projectId": "janagraha-cce3a",
    "storageBucket": "janagraha-cce3a.appspot.com",
    "messagingSenderId": "27343948050",
    "appId": "1:27343948050:web:563df56c0c4a90b2558bcb",
    "measurementId": "G-J7RS6NV8G2"
}

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()
database = firebase.database()

def getReferences():
    return auth, database
