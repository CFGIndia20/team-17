import datetime
import json
import time

import firebase_admin
from django.http import HttpResponse
from django.shortcuts import render
from firebase_admin import credentials, firestore
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from firebase import getReferences

from . import ml, utils

auth, database,bot = getReferences()
cred = credentials.Certificate("./fire1.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


GOT_LOCATION="We have noted the location of your complaint."
GOT_IMAGE="We have attached the above image to your complaint."
GOT_DESC="We have noted your description of the complaint and automatically categorized it for you!"
GOT_AUDIO="We have noted your audio-formatted complaint and automatically categorized it for you!"
GOT_VIDEO="We have noted your video-formatted complaint and automatically categorized it for you!"
SEND_LOCATION="Please share the location of the area of complaint"
SEND_IMAGE="Would you like to share an image corresponding to the complaint?"
SEND_DESC="Please describe the complaint in a few sentences."
END_MSG="Thank you for logging a complaint on I Change My City! You have done a great work as a citizen :)\nYou can track your complaint with the following number: "


@api_view(['GET', 'POST'])
def postComplaint(request):
    if request.method == 'GET':

        if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get("hub.challenge"):
            if not request.query_params.get("hub.verify_token") == "hello":
                return HttpResponse("Verification token mismatch", 403)
            return HttpResponse(request.query_params["hub.challenge"], 200)
        return HttpResponse("Hello world", 200)

    elif request.method == 'POST':

        received_json_data = json.loads(request.body.decode("utf-8"))
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
                            reply = firestore1('text', [listOfCategory[0],messaging_text], sender_id)
                        elif 'attachments' in messaging_event['message']:
                            attachment = messaging_event['message']['attachments'][0]
                            if attachment['type']=='audio':
                                audio = attachment['payload']['url']
                                text = utils.convert_to_text(audio)
                                listOfCategory = ml.predict([text])
                                firestore1('text', [listOfCategory[0], text], sender_id)
                                reply = firestore1('audio', audio,sender_id)
                            if attachment['type']=='video':
                                video = attachment['payload']['url']
                                text = utils.convert_to_text(video)
                                listOfCategory = ml.predict([text])
                                firestore1('text', [listOfCategory[0], text], sender_id)
                                reply = firestore1('video', video,sender_id)
                            if attachment['type']=='image':
                                image = attachment['payload']['url']
                                reply =firestore1('image', image,sender_id)
                            if attachment['type']=='location':
                                location = attachment['payload']['coordinates']
                                reply =firestore1('location', location, sender_id)
                        else:
                            messaging_text = 'no text'
                            reply="Okay"

                        bot.send_text_message(sender_id,reply)
        return HttpResponse("hi", 200)

def firestore1(type,data,sender_id):

    userId = sender_id
    # to update timestamp after each document update 
    now = time.time()
    # Realtime Database query 
    users = database.child("user").get()

    # this is not the first interaction for a new complaint
    if users.val() is not None:
        # search each user currently in the process of submitting a complainr
        for user in users.val():
            if user==userId:
                # complaint ID for updating the complaint
                complaintId = database.child("user").child(user).get().val()["complaint_id"]
                value = db.collection('user').document(user).collection("complaints").document(
                    complaintId).get().to_dict()
                # gave a description of complaint
                if type == 'text':
                    value["timestamp"] = now
                    value["text"] = data[1]
                    value["category"] = data[0]
                    # has not given the location
                    if value["lat"]==0 and value["long"]==0:
                        return " ".join([GOT_DESC, SEND_LOCATION])
                    # has given the location
                    else:
                        if value["image_url"]=='' and value["status"]==0:
                            value["status"] = 1
                            db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                            return " ".join([GOT_DESC, SEND_IMAGE])
                        else:
                            return " ".join([END_MSG, complaintId])
                if type == 'audio':
                    value["timestamp"] = now
                    value["audio_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return " ".join([GOT_AUDIO, SEND_LOCATION])
                    else:
                        if value["image_url"]=='' and value["status"]==0:
                            value["status"] = 1
                            db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                            return " ".join([GOT_AUDIO, SEND_IMAGE])
                        else:
                            return " ".join([END_MSG, complaintId])
                if type == 'video':
                    value["timestamp"] = now
                    value["video_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return " ".join([GOT_VIDEO, SEND_LOCATION])
                    else:
                        return " ".join([END_MSG, complaintId])
                if type == 'image':
                    value["timestamp"] = now
                    value["image_url"] = data
                    db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                    if value["lat"]==0 and value["long"]==0:
                        return " ".join([GOT_IMAGE, SEND_LOCATION])
                    else:
                        if value["text"]=='':
                            return " ".join([GOT_IMAGE, SEND_DESC])
                        else:
                            return " ".join([END_MSG, complaintId])
                if type == 'location':
                    value["timestamp"] = now
                    value["lat"] = data["lat"]
                    value["long"] = data["long"]
                    if value["text"]=='':
                        return " ".join([GOT_LOCATION, SEND_DESC])
                    else:
                        if value["image_url"]=='' and value["status"]==0:
                            value["status"] = 1
                            db.collection('user').document(user).collection("complaints").document(complaintId).set(value)
                            return " ".join([GOT_LOCATION, SEND_IMAGE])
                        else:
                            return " ".join([END_MSG, complaintId])
                return "None"
    # this is the first interaction for a new complain
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
        reply=''
        if type == 'text':
            value["timestamp"] = now
            value["text"] = data[1]
            value["category"] = data[0]
            reply = " ".join([GOT_DESC, SEND_LOCATION])
        if type == 'audio':
            value["timestamp"] = now
            value["audio_url"] = data
            reply = " ".join([GOT_AUDIO, SEND_LOCATION])
        if type == 'video':
            value["timestamp"] = now
            value["video_url"] = data
            reply = " ".join([GOT_VIDEO, SEND_LOCATION])
        if type == 'image':
            value["timestamp"] = now
            value["image_url"] = data
            reply = " ".join([GOT_IMAGE, SEND_DESC])
        if type == 'location':
            value["timestamp"] = now
            value["lat"] = data["lat"]
            value["long"] = data["long"]
            reply = " ".join([GOT_LOCATION, SEND_DESC])
        doc_ref = db.collection('user').document(userId).collection("complaints")

        val = doc_ref.add(value)
        key = val[1].id

        database.child("user").child(userId).set({'complaint_id': key})
        return reply