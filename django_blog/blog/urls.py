from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path("logout/", views.logout_view, name="logout"),
    path("", views.PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/update/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("search/", views.SearchResultsView.as_view(), name="search"),
    path("tags/<slug:tag_slug>/", views.PostsByTagListView.as_view(), name="posts-by-tag"),
]