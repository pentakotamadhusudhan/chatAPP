from django.urls import path
from . import views
from .chatcrud import ChatViews,ChatListViews,GetFriendsListView

urlpatterns = [
    path('', views.index, name='index'),
    path('count', views.count, name='count'),
    path('user', views.UserCreateView.as_view(), name='user_create'),
    path('login', views.UserLoginView.as_view(), name='UserLoginView'),
    path('getfriends', GetFriendsListView.as_view(), name='getfirends'),
    path('getfriend/<int:friendID>',views.GetFriendByIDView.as_view(), name='getfirendByID'),
    path('sendmessage', ChatViews.as_view(), name='sendmessage'),
    path('getmessages/fromuser:<int:from_user>/touser:<int:to_user>/', ChatListViews.as_view(), name='getmessages'),
]
