from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics
from .models import FriendsModel
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
    queryset = UserProfile.objects.all()

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
    queryset = UserProfile.objects.all()

    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            print("Username received:", username)
            print("Password received:", password)

            # user = authenticate(username=username, password=password)
            user = UserProfile.objects.get(username=username, password=password)
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
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self,request,friendID):
        print(friendID)
        queryset = UserProfile.objects.get(id=friendID)
        ser = self.serializer_class(queryset)
        response = returnresponse(status_code=200,data=ser.data,message="friend founded")
        return Response(response, status=status.HTTP_200_OK)
    

class FriendRequestView(generics.GenericAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendsModel.objects.all()

    def post(self, request):
        logger.info(f"Received data: {request.data}")
       
        try:
            serializer = self.serializer_class(data=request.data)
            print("Received data",request.data)
            if serializer.is_valid():
                print("Rebdbbd bsd")
                
                user = serializer.save()
                response = returnresponse(status_code=200,data=serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            else:
            
                logger.warning(f"Serializer validation failed: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            logger.error(f"Error creating user: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class FriendRequestUpdateView(generics.GenericAPIView):

    serializer_class = FriendRequestSerializer
    queryset = FriendsModel.objects.all()

    def put(self, request, friendRequestID):
        try:
            friend_data =  get_object_or_404(FriendsModel,id = friendRequestID)
            serializer = self.serializer_class(instance= friend_data,data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = returnresponse(status_code=200,data=serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error updating friend request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class FindFriendsView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self,request,):
        queryset = UserProfile.objects.all()
        ser = self.serializer_class(queryset,many=True)
        response =  returnresponse(status_code=200,data=ser.data,message="Message sent successfully")
        return Response(response, status=status.HTTP_201_CREATED)



class GetFriendsListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self,request,):
        li = []
        friend_list =  FriendsModel.objects.filter(user1_id = 1, is_friend =False)
        
        for i in friend_list:
            # queryset = UserProfile.objects.get(id =i.user2)
            li.append(i.user2)
        ser = UserSerializer(li,many=True)
        response =  returnresponse(status_code=200,data=ser.data,message="Message sent successfully")
        return Response(response, status=status.HTTP_201_CREATED)