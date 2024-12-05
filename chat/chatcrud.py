from .models import ChatModel
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ChatPostSerializers,UserSerializer
from NewChatProject.genericresponse import returnresponse
from rest_framework import status
from NewChatProject.genericresponse import returnresponse
from django.contrib.auth.models import User
from django.db.models import Q


class GetFriendsListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self,request,):
        queryset = User.objects.all()
        ser = self.serializer_class(queryset,many=True)
        response =  returnresponse(status_code=200,data=ser.data,message="Message sent successfully")
        return Response(response, status=status.HTTP_201_CREATED)


class ChatViews(generics.GenericAPIView):
    queryset = ChatModel.objects.all()
    serializer_class = ChatPostSerializers

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response =  returnresponse(status_code=200,data=None,message="Message sent successfully")
        return Response(response, status=status.HTTP_201_CREATED)



class ChatListViews(generics.ListAPIView):
    queryset = ChatModel.objects.all()
    serializer_class = ChatPostSerializers

    def get(self,request,from_user,to_user):
        queryset = ChatModel.objects.filter(Q(from_user=1, to_user=2) | Q(from_user=2, to_user=1)).order_by("-timestamp")
        ser = self.serializer_class(queryset,many=True)
        return Response(
            {
                "data": ser.data,
                "status":200
            }
        )


