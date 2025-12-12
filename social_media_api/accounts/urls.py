from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView, FollowUserView, 
    UnfollowUserView, FollowersListView, FollowingListView
    )

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("follow/<int:user_id>/", FollowUserView.as_view()),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view()),
    path("users/<int:user_id>/followers/", FollowersListView.as_view()),
    path("users/<int:user_id>/following/", FollowingListView.as_view()),
]