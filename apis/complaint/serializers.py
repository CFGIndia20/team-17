# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
# from firebase import getReferences
# # Create your views here.
# auth, database = getReferences()


# # @api_view(['GET', 'POST'])
# # def complaint_list(request):
# #     """
# #     List all code snippets, or create a new snippet.
# #     """
# #     if request.method == 'GET':
# #         snippets = Snippet.objects.all()
# #         serializer = SnippetSerializer(snippets, many=True)
# #         return Response(serializer.data)

# #     elif request.method == 'POST':
# #         serializer = SnippetSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             value={
# #                 "text":"There is a lot of garbage in my area",
# #                 "lat":78.92,
# #                 "long":93.76,
# #                 "category":"Garbage Collection",
# #                 "user_identity":"1"
# #             }

# #             database.child('user').child("complaints").push(value)
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)