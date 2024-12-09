from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import ChatModel,UserProfile,FriendsModel


class UserSerializer(ModelSerializer):  
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None

    # class Meta:
    #     model = UserProfile
    #     fields = ['profile_image', 'bio', 'dob', 'nick_name']
    class Meta:
        model = UserProfile
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }
    
class LoginSerializer(ModelSerializer):  
    class Meta:
        model = UserProfile
        fields = "username",'password'
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
        }


class ChatPostSerializers(ModelSerializer):  
    class Meta:
        model = ChatModel
        fields = "__all__"
       


class FriendRequestSerializer(ModelSerializer):  
    class Meta:
        model = FriendsModel
        fields = "__all__"
       
       