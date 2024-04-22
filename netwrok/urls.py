# urls.py
from django.urls import path
from .views import ( UserSignup,UserSearchAPIView, FriendshipRequestAPIView, 
                    FriendsListAPIView, PendingFriendRequestsAPIView, FriendshipRequestRespondAPIView
)
from rest_framework.authtoken import views as authviews

urlpatterns = [
    path('signup/', UserSignup.as_view({'post': 'create'}), name='signup'),
    path('login/',authviews.obtain_auth_token),
    path('search/', UserSearchAPIView.as_view(), name='user_search'),
    path('send-friend-request/', FriendshipRequestAPIView.as_view(), name='friend_request'),
    path('friends-list/', FriendsListAPIView.as_view(), name='friends_list'),
    path('pending-requests/', PendingFriendRequestsAPIView.as_view(), name='pending_requests'),
    path('friend-request-respond/',FriendshipRequestRespondAPIView.as_view(), name='request-respond')
]