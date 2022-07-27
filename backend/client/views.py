from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize

from user.models import User
from user.serializers import UserSerializer

# Create your views here.
class ClientPageView(APIView):
    """ Client profile dashboard """

    """ User data"""
    def get(self,request):
        user=get_object_or_404(User,id=request.user.id)

        if user:
            serializer=UserSerializer(data=user)
            return Response(serializer)


    """ User address"""
    def put(self,request):
        
        user=get_object_or_404(User,request.user.id)

        if user:
            serializer=UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

