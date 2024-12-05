
from django.shortcuts import render
from rest_framework import generics

from NewChatProject.genericresponse import returnresponse
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import logging

# Create your views here.
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def count(request):
    return render(request, 'count.html')


logger = logging.getLogger(__name__)

class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        logger.info(f"Received data: {request.data}")
        try:
            # Create serializer instance with the incoming data
            serializer = self.serializer_class(data=request.data)
            # Validate serializer
            if serializer.is_valid():
                # Save the user (serializer will automatically handle password hashing)
                user = serializer.save()

                # Log the successful user creation
                logger.info(f"User created successfully: {user.username}")

                # Return the serialized user data (response can include user details or token)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Log the validation errors
                logger.warning(f"Serializer validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the exception details for debugging
            logger.error(f"Error creating user: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            print("Username received:", username)
            print("Password received:", password)

            # user = authenticate(username=username, password=password)
            user = User.objects.get(username=username, password=password)
            print("Password:", user)

            if user is not None:
                serializer = UserSerializer(user)
                if serializer:
                  
                    # return Response(serializer.data, status=status.HTTP_200_OK)

                    response =  returnresponse(status_code=200,data=serializer.data,message="Login successful")
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                    response =  returnresponse(status_code=400,data=serializer.data,message=serializer.error)
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(f"Error during login: {str(e)}")
            # return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            response =  returnresponse(status_code=500,data=None,message=e.args[0])
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        






class GetFriendByIDView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self,request,friendID):
        print(friendID)
        queryset = User.objects.get(id=friendID)
        ser = self.serializer_class(queryset)
        response = returnresponse(status_code=200,data=ser.data,message="friend founded")
        return Response(response, status=status.HTTP_200_OK)