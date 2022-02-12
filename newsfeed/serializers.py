from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from newsfeed.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    likes = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'body', 'likes', 'user']
        read_only_fields = ['user']

    def get_likes(self, post_instance):
        likes = PostLike.objects.filter(post_id=post_instance.id).values_list('user', flat=True)
        return likes


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['id', 'post', 'created_at']

