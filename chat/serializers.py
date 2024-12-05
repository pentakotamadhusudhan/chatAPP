from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import ChatModel


class UserSerializer(ModelSerializer):  
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }
    
class LoginSerializer(ModelSerializer):  
    class Meta:
        model = User
        fields = "username",'password'
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }


class ChatPostSerializers(ModelSerializer):  
    class Meta:
        model = ChatModel
        fields = "__all__"
       