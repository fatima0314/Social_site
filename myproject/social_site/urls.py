from django.urls import path
from .views import *


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('users/', UserProfileApiView.as_view(),name = 'users'),
    path('users/<int:pk>/', UserProfileEditApiView.as_view(), name = 'user_edit'),
    path('posts/', PostApiView.as_view(), name = 'posts'),
    path('posts/create/', PostCreateApiView.as_view(), name = 'post_create'),
    path('posts/<int:pk>/', PostEditApiView.as_view(), name = 'post_edit'),
    path('posts/comment/<int:pk>/', CommentApiView.as_view(), name = 'comment'),
    path('follows/<int:pk>/', FollowApiView.as_view(), name = 'follows' ),
    path('story/<int:pk>/', StoryApiView.as_view(), name = 'story'),
    path('posts/comment_likes/<int:pk>/', CommentLikeApiView.as_view(), name ='comment_like'),
    path('posts/likes/<int:pk>/', PostLikeApiView.as_view(), name='post_likes'),
    path('save_items/', SaveItemApiView.as_view(), name = 'save_items')
]