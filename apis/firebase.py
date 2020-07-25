import pyrebase
from pymessenger import Bot
firebaseconfig = {
    "apiKey": "AIzaSyAH1hNhcetH_YvEalGRRjCIJPQXRNeUg_o",
    "authDomain": "labcoordinator-b2bb3.firebaseapp.com",
    "databaseURL": "https://labcoordinator-b2bb3.firebaseio.com",
    "projectId": "labcoordinator-b2bb3",
    "storageBucket": "labcoordinator-b2bb3.appspot.com",
    "messagingSenderId": "602115928200",
    "appId": "1:602115928200:web:2d6a59967fdd781e626f3d",
    "measurementId": "G-3BK35C41MG"

}

PAGE_ACCESS_TOKEN = "EAA09YRWYyQUBAMrjyLJBDcqygPbaDHgvPNYVQtLsZC2rsXONec2j4Iqu9b4WKaXBJ6nW9THC4Qs7DN4ZCxFb0zLljpZBTa6bIk28CXXJnMUgqRxcxglskfuVWCjb9jP2KZBI8FBrVUk1xOqn2vFzKEqwZBr4Cqk2vapcJSyPuacpSEpjJQtLj"

bot = Bot(PAGE_ACCESS_TOKEN)

firebase = pyrebase.initialize_app(firebaseconfig)
auth = firebase.auth()
database = firebase.database()

def getReferences():


    return auth, database,bot
