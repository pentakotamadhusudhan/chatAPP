from django.urls import path
from . import views
from .chatcrud import ChatViews,ChatListViews
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('', views.index, name='index'),
    path('count', views.count, name='count'),
    path('user', views.UserCreateView.as_view(), name='user_create'),
    path('login', views.UserLoginView.as_view(), name='UserLoginView'),
    path('getfriends', views.GetFriendsListView.as_view(), name='getfirends'),
    path('findfriends', views.FindFriendsView.as_view(), name='findfirends'),
    path('getfriend/<int:friendID>',views.GetFriendByIDView.as_view(), name='getfirendByID'),
    path('sendmessage', ChatViews.as_view(), name='sendmessage'),
    path('getmessages/fromuser:<int:from_user>/touser:<int:to_user>/', ChatListViews.as_view(), name='getmessages'),
    path('friendrequest', views.FriendRequestView.as_view(), name='friend_request'),
    path('friendrequestupdate/<int:friendRequestID>', views.FriendRequestUpdateView.as_view(), name='friend_request_update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))