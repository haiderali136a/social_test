from django.db import models
from django.utils.timezone import now

from user.models import UserProfile


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)


class PostLike(models.Model):
    class Meta:
        unique_together = (('user', 'post'),)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(default=now)


