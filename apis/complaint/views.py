from django.shortcuts import render
from firebase import getReferences
# Create your views here.
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
auth, database,bot = getReferences()
from . import ml


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./fire1.json")
firebase_admin.initialize_app(cred)
db = firestore.client()





@api_view(['GET', 'POST'])
def postComplaint(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # snippets = Snippet.objects.all()
        # # serializer = SnippetSerializer(snippets, many=True)
        if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
            if not request.query_params.get("hub.verify_token") == "hello":
                return HttpResponse("Verification token mismatch", 403)
            print("***********************",request.query_params["hub.challenge"])
            return HttpResponse(request.query_params["hub.challenge"], 200)
        return HttpResponse("Hello world", 200)
        # print(request.data,request.query_params)
        # return Response("Hello", 200)

    elif request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)
        print("***********************")

        # data = request.get_json()
        #
        # print(data)



        print(request.data["object"])


        data=request.data

        if data['object'] == 'page':
            for entry in data['entry']:
                for messaging_event in entry['messaging']:

                    # IDs
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']

                    if messaging_event.get('message'):
                        # Extracting text message
                        if 'text' in messaging_event['message']:
                            messaging_text = messaging_event['message']['text']
                            listOfCategory = ml.predict([messaging_text])

                            ##### add lat long
                            value = {
                                "text": messaging_event['message']['text'],
                                "lat": 78.92,
                                "long": 93.76,
                                "category": "Garbage Collection",
                                "user_identity": sender_id
                            }

                            database.child('user').child("complaints").push(value)
                        else:
                            messaging_text = 'no text'

                        # Echo
                        response = messaging_text
                        bot.send_text_message(sender_id, listOfCategory[0])
        print(request.data)
        print("^^^^^^^^^^^^^^^^^^")
        return HttpResponse("hi", 200)
        # return HttpResponse(request.data, 200)


def firestore1(request):

    userId = "123456"



    users = database.child("user").get()

    for user in users.val():

        if user['id']==userId:
            long = 10.67
            value = db.collection('user').document(user['id']).collection("complaints").get().to_dict()

            print("%%%%%%%%%%%%%%5")
            value["long"]=long
            db.collection('user').document(user['id']).collection("complaints").set(value)

        else:

            doc_ref = db.collection('user').document(userId).collection("complaints")

            val = doc_ref.add({
                'text': 'This is bad area',
                'lat': 20.78,
                'long': 40.67,
                'category': "Garbage",
                "status": 0

            })

            ###addkey
            key = val[1].id
            print("^^^^^^^^^^^^^^^^^^^^^^6", val[1].id)

            database.child("user").child(userId).set({'complaint_id': key})



    return HttpResponse("done")


