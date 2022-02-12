import random

import requests

from config import number_of_users, max_posts_per_user, max_likes_per_user, DEFAULT_HOST


class SocialBot:

    def __init__(self, users_count, max_posts_user, max_likes_user):
        self.number_of_users = users_count
        self.max_posts_per_user = max_posts_user
        self.max_likes_per_user = max_likes_user
        self.user_details = dict()
        self.post_count_by_user = dict()
        self.auth_headers = []

    def signup_users(self):  # for registering users
        signup_url = f'{DEFAULT_HOST}user/signup'
        for i in range(0, self.number_of_users):
            payload = {
                "first_name": "xyz", "last_name": "abc", "email": f"abc{i}@gmail.com",
                "username": f"abc{i}", "password": "user12345678"
            }
            resp = requests.post(signup_url, data=payload)
            if resp.status_code == 201:
                resp_data = resp.json()
                print(f"User with email: {payload['email']} created successfully!")
                self.user_details[resp_data['id']] = payload

    def login_user(self, user_details):         # for logging-in a single user
        login_url = f'{DEFAULT_HOST}user/login'
        resp = requests.post(login_url, data=user_details)
        auth_token = resp.json()['access']
        return auth_token

    def login_all_users(self):  # for logging-in all users
        for item in self.user_details:
            payload = self.user_details[item]
            user_token = self.login_user(payload)
            self.user_details[item]['access'] = user_token

    def create_posts(self):  # for creating user_posts
        for item in self.user_details:
            rand = random.randint(1, self.max_posts_per_user)
            create_post_url = f'{DEFAULT_HOST}newsfeed/post/create'
            for j in range(0, rand):
                resp = requests.post(create_post_url, data={'body': f"Hey there {random.randint(1, 1000)}"},
                                     headers={'Authorization': f'Bearer {self.user_details[item]["access"]}'})
            print(f"{rand} posts created for user {item}")

    def get_likes_by_users(self):          # for getting likes for posts, by users
        newsfeed_url = f'{DEFAULT_HOST}newsfeed'
        resp = requests.get(newsfeed_url)
        resp_data = resp.json()
        likes_by_user = dict()
        for post in resp_data:
            if post['user'] in likes_by_user:
                likes_by_user[post['user']] += [len(post['likes'])]
            else:
                likes_by_user[post['user']] = [len(post['likes'])]
        return likes_by_user

    def get_user_with_max_likes(self):          # for getting likes for posts, by users
        max_likes_sent = list()
        newsfeed_url = f'{DEFAULT_HOST}newsfeed'
        resp = requests.get(newsfeed_url)
        resp_data = resp.json()
        likes_by_user = dict()
        for post in resp_data:
            for like in post['likes']:
                if like in likes_by_user:
                    likes_by_user[like] += 1
                else:
                    likes_by_user[like] = 1

        sorted_likes_by_user = dict(sorted(likes_by_user.items(), key=lambda x: x[1], reverse=True))
        for user in sorted_likes_by_user.copy():
            if sorted_likes_by_user[user] >= self.max_likes_per_user:
                max_likes_sent.append(user)
        return max_likes_sent

    def get_user_with_max_post_count(self):
        sorted_post_count = dict(sorted(self.post_count_by_user.items(), key=lambda x: x[1], reverse=True))
        max_like_users = self.get_user_with_max_likes()
        for user in sorted_post_count.copy():
            if user not in max_like_users:
                return user
        return -1

    def get_post_count_by_user(self):
        newsfeed_url = f'{DEFAULT_HOST}newsfeed'
        resp = requests.get(newsfeed_url)
        resp_data = resp.json()
        for post in resp_data:
            if post['user'] in self.post_count_by_user:
                self.post_count_by_user[post['user']] += 1
            else:
                self.post_count_by_user[post['user']] = 1

    def get_user_with_post_with_no_likes(self, likes_by_users, exclude_user):
        # for fetching users with post having 0 likes
        for user in likes_by_users:
            if user == exclude_user:
                continue
            for likes in likes_by_users[user]:
                if likes == 0:
                    return user
        return -1

    def like_random_post(self, user_liker, user_being_liked):  # for liking a random post of a specific user
        user_posts_url = f'{DEFAULT_HOST}newsfeed/{user_being_liked}'
        post_like_url = f'{DEFAULT_HOST}newsfeed/post/like'
        posts = requests.get(user_posts_url)
        posts = posts.json()
        auth_token = self.login_user(self.user_details[user_liker])
        random.shuffle(posts)
        for post in posts:
            payload = {'post': post['id']}
            resp = requests.post(post_like_url, json=payload,
                                 headers={'Authorization': f'Bearer {auth_token}'})
            if resp.status_code == 201:
                break

    def start_bot(self):                        # for starting bot execution
        self.signup_users()
        print("Users registered!!\n")
        self.login_all_users()
        self.create_posts()
        print("Posts Created!!\n")
        while True:
            self.get_post_count_by_user()
            likes_by_user = self.get_likes_by_users()
            get_next_user = self.get_user_with_max_post_count()
            print(f"Next User (with max posts): {get_next_user}")
            user = self.get_user_with_post_with_no_likes(likes_by_user, get_next_user)
            if user == -1:
                break
            print(f"User (with a post with 0 likes): {user}")
            self.like_random_post(user_liker=get_next_user, user_being_liked=user)


social_bot = SocialBot(users_count=number_of_users, max_likes_user=max_likes_per_user, max_posts_user=max_posts_per_user)
social_bot.start_bot()
