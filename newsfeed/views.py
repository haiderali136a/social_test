from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from newsfeed.models import Post, PostLike
from newsfeed.serializers import PostSerializer, PostLikeSerializer


class PostCreateView(CreateAPIView):

    model = Post
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostListView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (AllowAny, )


class PostLikeToggleView(generics.CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            return Response({"message": "Post unliked successfully"}, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        post = serializer.validated_data['post']
        if post.user == self.request.user:
            raise Exception("You cannot like your own post!!!")
        try:
            serializer.save()
        except IntegrityError as e:
            postlike_obj = PostLike.objects.filter(post=post, user=self.request.user).first()
            postlike_obj.delete()
            post.likes = max(post.likes - 1, 0)
            post.save()
            raise IntegrityError
        post.likes += 1
        post.save()
