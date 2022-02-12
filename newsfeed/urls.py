from django.urls import path
from newsfeed.views import PostCreateView, PostListView, PostLikeToggleView, UserPostListView, PostLikeView

urlpatterns = [
    path('post/create', PostCreateView.as_view(), name='create-post'),
    path('', PostListView.as_view(), name='all-posts'),
    path('<int:user>', UserPostListView.as_view(), name='user-all-posts'),
    path('post/like', PostLikeView.as_view(), name='like-post'),
    path('post/like_toggle', PostLikeToggleView.as_view(), name='toggle-like-post'),
]
