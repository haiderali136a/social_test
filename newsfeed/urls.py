from django.urls import path
from newsfeed.views import PostCreateView, PostListView, PostLikeToggleView

urlpatterns = [
    path('post/create', PostCreateView.as_view(), name='create-post'),
    path('', PostListView.as_view(), name='all-posts'),
    path('post/like', PostLikeToggleView.as_view(), name='like-post'),
]
