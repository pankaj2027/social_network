from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate,login
from .serializers import UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import User, Friendship
from .serializers import UserSerializer, FriendshipSerializer,FriendshipRespondSerializer
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


# User sign up
class UserSignup(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':"Your registration has been completed Successfully!!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSearchAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            return User.objects.filter(Q(email__iexact=keyword) | Q(first_name__icontains=keyword) ).distinct()
        return User.objects.none()


class FriendshipRequestAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        from_user = request.user
        to_user_id = serializer.validated_data.get('to_user')
        if from_user.id == to_user_id.id:
            return Response({'error': 'You cannot send friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if Friendship.objects.filter(from_user=from_user, to_user_id=to_user_id).exists():
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)
        if Friendship.objects.filter(from_user_id=to_user_id, to_user=from_user, is_accepted=False).exists():
            return Response({'error': 'Friend request already received.'}, status=status.HTTP_400_BAD_REQUEST)
        if Friendship.objects.filter(from_user=from_user, created_at__gte=timezone.now() - timedelta(minutes=1)).count() >= 3:
            return Response({'error': 'You cannot send more than 3 friend requests within a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FriendsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        friend_requests = Friendship.objects.filter(to_user=user, is_accepted=True)
        friend_ids = list()
        for fr in friend_requests:
            if fr.from_user == user:
                friend_ids.append(fr.to_user.id)
            else:
                friend_ids.append(fr.from_user.id)
        # Querying for users based on those IDs
        friends = User.objects.filter(id__in=friend_ids)
        return friends

class PendingFriendRequestsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        pending_requests = Friendship.objects.filter(to_user=user, is_accepted=False)
        return pending_requests
    
class FriendshipRequestRespondAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipRespondSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        is_accepted = serializer.validated_data.get('is_accepted')
        to_user = serializer.validated_data.get('to_user')
        updated_data = Friendship.objects.filter(to_user=to_user, from_user=user,is_accepted=False).update(is_accepted=True)
        if updated_data:
            msg = "Friend request Accepted" if is_accepted else "Friend request Rejected"
            return Response({"message": msg}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No Friend Request"}, status=status.HTTP_404_NOT_FOUND)