from django.shortcuts import render
from firebase import getReferences
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
auth, database = getReferences()


@api_view(['GET', 'POST'])
def postComplaint(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # snippets = Snippet.objects.all()
        # # serializer = SnippetSerializer(snippets, many=True)
        # if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        #     if not request.args.get("hub.verify_token") == "hello":
        #         return "Verification token mismatch", 403
        #     return request.args["hub.challenge"], 200
        return "Hello world", 200
        # return Response("Hello world", 200)

    elif request.method == 'POST':

        value={
        "text":"There is a lot of garbage in my area",
        "lat":78.92,
        "long":93.76,
        "category":"Garbage Collection",
        "user_identity":"1"
        }

        database.child('user').child("complaints").push(value)

        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
            if not request.args.get("hub.verify_token") == "hello":
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "Hello world", 200
        # return HttpResponse(request.data)
        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# def postComplaint(request):

#     value={
#         "text":"There is a lot of garbage in my area",
#         "lat":78.92,
#         "long":93.76,
#         "category":"Garbage Collection",
#         "user_identity":"1"
#     }

#     database.child('user').child("complaints").push(value)

#     return HttpResponse('Inserted')



