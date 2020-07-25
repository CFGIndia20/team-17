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
from . import utils
import datetime
import time
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
                            # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",listOfCategory[0])
                            reply = firestore1('text', [listOfCategory[0],messaging_text], sender_id)

                        elif 'attachments' in messaging_event['message']:

                            # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

                            attachment = messaging_event['message']['attachments'][0]
                            if attachment['type']=='audio':
                                audio = attachment['payload']['url']
                                text = utils.convert_to_text(audio)

                                print("82")
                                print(text)
                                listOfCategory = ml.predict([text])
                                # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",listOfCategory[0])
                                firestore1('text', [listOfCategory[0], text], sender_id)
                                reply = firestore1('audio', audio,sender_id)
                            if attachment['type']=='video':
                                video = attachment['payload']['url']

                                text = utils.convert_to_text(video)

                                print("82")
                                print(text)
                                listOfCategory = ml.predict([text])
                                firestore1('text', [listOfCategory[0], text], sender_id)
                                reply = firestore1('video', video,sender_id)
                            if attachment['type']=='image':
                                image = attachment['payload']['url']
                                reply =firestore1('image', image,sender_id)
                            if attachment['type']=='location':
                                location = attachment['payload']['coordinates']


                                # print("blahhhhhhhhhhh",location)
                                reply =firestore1('location', location, sender_id)





                        else:
                            messaging_text = 'no text'
                            reply="Niral"
                        # Echo
                        # response = messaging_text

                        # print("***************************************************************",sender_id)
                        # bot.send_text_message('3116019708516943', "hi niral")
                        bot.send_text_message(sender_id,reply)



        print(request.data)
        print("^^^^^^^^^^^^^^^^^^")
        return HttpResponse("hi", 200)
        # return HttpResponse(request.data, 200)



def trythis():

    bot.send_text_message('3116019708516943', "hi niraj")


def firestore1(type,data,sender_id):

    userId = sender_id

    now = datetime.datetime.now().strftime('%H:%M:%S')
    now = time.time()
    #Realtime
    users = database.child("user").get()

    if users.val() is not None:
        for user in users.val():
            # print(type(user))
            if user==userId:

                complaintId = database.child("user").child(user).get().val()["complaint_id"]

                value = db.collection('user').document(user).collection("complaints").document(
                    complaintId).get().to_dict()
                if type == 'text':
                    value["timestamp"] = now
                    print("140")
                    value["text"] = data[1]
                    value["category"] = data[0]
                    if value["lat"]==0 and value["long"]==0:
                        return "Send Location"
                    else:
                        return complaintId
                if type == 'audio':
                    value["timestamp"] = now
                    # print("%%%%%%%777777777777%%%%%%%5")
                    # print(complaintId)
                    value["audio_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return "Send Location"
                    else:
                        return complaintId
                if type == 'video':
                    value["timestamp"] = now
                    value["video_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return complaintId
                    else:
                        return "Send Location"
                if type == 'image':
                    value["timestamp"] = now
                    value["image_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return complaintId
                    else:
                        return "Send Location"
                if type == 'location':
                    print(data)
                    value["timestamp"] = now
                    value["lat"] = data["lat"]
                    value["long"] = data["long"]

                return "None"
                # long = 1000.89


                # print("%%%%%%%%%%%%%%5")




    else:

        value = {
            'text': '',
            'image_url': '',
            'video_url': '',
            'lat': 0.0,
            'long': 0.0,
            'category': "",
            "status": 0,
            'audio_url': '',
            'timestamp':now

        }
        if type == 'text':
            value["timestamp"] = now
            print("212")
            value["text"] = data[1]
            value["category"] = data[0]
        if type == 'audio':
            value["timestamp"] = now
            # print("%%%%%%%777777777777%%%%%%%5")
            value["audio_url"] = data
        if type == 'video':
            value["timestamp"] = now
            value["video_url"] = data
        if type == 'image':
            value["timestamp"] = now
            value["image_url"] = data
        if type == 'location':
            print(data)
            value["timestamp"] = now
            value["lat"] = data["lat"]
            value["long"] = data["long"]
        doc_ref = db.collection('user').document(userId).collection("complaints")

        val = doc_ref.add(value)

        ###addkey
        key = val[1].id
        print("^^^^^^^^^^^^^^^^^^^^^^6", val[1].id)

        database.child("user").child(userId).set({'complaint_id': key})



    # return HttpResponse("done")


