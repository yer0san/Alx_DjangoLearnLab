from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import CustomUser

from notification.utils import create_notification


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = user.auth_token.key
            return Response({
                'user': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        user = request.user

        if user == target:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        if target in user.following.all():
            return Response({"detail": "Already following this user."}, status=400)

        user.following.add(target)
        create_notification(
            recipient=target,
            actor=user,
            verb="started following you",
            target=target
        )
        return Response({"detail": f"You are now following {target.username}."}, status=200)
        
        


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, id=user_id)
        user = request.user

        if target not in user.following.all():
            return Response({"detail": "You are not following this user."}, status=400)

        user.following.remove(target)
        return Response({"detail": f"Unfollowed {target.username}."}, status=200)


class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)


class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)

# accounts/views.py doesn't contain: ["generics.GenericAPIView", "CustomUser.objects.all()"], but i don't like generics.GenericAPIView

from rest_framework import generics
class SomeGenericClass(generics.GenericAPIView):
    users = CustomUser.objects.all()
    pass
# i don't feel like refactoring everything to genericsAPIView :)
