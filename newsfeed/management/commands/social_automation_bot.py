import random

from django.core.management import BaseCommand
import requests
from django.db.models import Count

from SocialNetworkTest.settings import DEFAULT_HOST
from config import number_of_users, max_posts_per_user, max_likes_per_user
from newsfeed.models import PostLike, Post
from user.models import UserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        run_bot()


def run_bot():
    signup_users()
    print("Users registered!!\n")
    auth_headers = login_users()
    create_posts(auth_headers)
    print("Posts Created!!\n")
    while True:
        grouped_posts = Post.objects.values('user').annotate(post_count=Count('id'))
        likes_by_user = PostLike.objects.values('user').annotate(likes_count=Count('id')).filter(
            likes_count__gt=max_likes_per_user).values_list('user', flat=True)
        get_next_user = grouped_posts.exclude(user__in=likes_by_user).order_by('-post_count').first()['user']
        print(f"Next User (with max posts): {get_next_user}")
        user = get_user_with_posts_without_likes(likes_by_user, get_next_user)
        if user == -1:
            break
        user_obj = UserProfile.objects.filter(pk=get_next_user).first()
        print(f"User (with a post with 0 likes): {user_obj.id}")
        like_random_post(user_obj, user)


def like_random_post(user_liker, user_being_liked):
    post = Post.objects.filter(user=user_being_liked)
    postlike = None
    for p in post:
        postlike = PostLike.objects.filter(post=p.id, user=user_liker).first()
        if not postlike:
            post = p
            break
    if postlike:
        return
    login_url = f'{DEFAULT_HOST}user/login'
    payload = {
            "email": user_liker.email,
            "username": user_liker.username, "password": "user12345678"
        }
    resp = requests.post(login_url, data=payload)
    auth_token = resp.json()['access']
    post_like_url = f'{DEFAULT_HOST}newsfeed/post/like'
    post_like_payload = {'post': post.id}
    print(f"User {user_liker.id} likes post with id: {post.id}")
    res = requests.post(post_like_url, data=post_like_payload, headers={'Authorization': f'Bearer {auth_token}'})
    pass


def get_user_with_posts_without_likes(exclude_list, user):
    for i in range(0, number_of_users):
        posts = Post.objects.filter(user=(i+1)).exclude(user__in=exclude_list, user=user).values_list('id', flat=True)
        for post in posts:
            postlike = PostLike.objects.filter(post=post)
            if not postlike:
                return i + 1
    return -1


def signup_users():
    # registering users
    signup_url = f'{DEFAULT_HOST}user/signup'
    for i in range(0, number_of_users):
        payload = {
            "first_name": "xyz", "last_name": "abc", "email": f"abc{i}@gmail.com",
            "username": f"abc{i}", "password": "user12345678"
        }
        resp = requests.post(signup_url, data=payload)


def login_users():
    # logging-in users
    auth_headers = []
    login_url = f'{DEFAULT_HOST}user/login'
    for i in range(0, number_of_users):
        payload = {
            "email": f"abc{i}@gmail.com",
            "username": f"abc{i}", "password": "user12345678"
        }
        resp = requests.post(login_url, data=payload)
        auth_token = resp.json()['access']
        auth_headers.append(auth_token)
    return auth_headers


def create_posts(auth_headers):
    for i in range(0, number_of_users):
        rand = random.randint(0, max_posts_per_user)
        create_post_url = f'{DEFAULT_HOST}newsfeed/post/create'
        for j in range(0, rand):
            resp = requests.post(create_post_url, data={'body': f"Hey there {i*23%2}"},
                                 headers={'Authorization': f'Bearer {auth_headers[i]}'})