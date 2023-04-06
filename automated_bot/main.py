from dotenv import load_dotenv
import os
import asyncio
import aiohttp
import random
import string

load_dotenv('.env.bot')

NUMBER_OF_USERS = int(os.environ.get("NUMBER_OF_USERS"))
MAX_POSTS_PER_USER = int(os.environ.get("MAX_POSTS_PER_USER"))
MAX_LIKES_PER_USER = int(os.environ.get("MAX_LIKES_PER_USER"))


class User:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.token = "token"

    async def get_last_post(self):
        url = "http://127.0.0.1:8000/post/get_last_post/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    id = await response.json()
                    return id[0]
                else:
                    print(f'ERROR: get_last_post')

    async def register(self):
        url = "http://127.0.0.1:8000/auth/register"
        payload = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status != 201:
                    print(f'Registration failed for user {self.username}')

    async def login(self):
        url = "http://127.0.0.1:8000/auth/jwt/login"
        payload = f"grant_type=&username={self.email}&password={self.password}&scope=&client_id=&client_secret="
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=payload) as response:
                if response.status == 200:
                    self.token = response.cookies.get("blog_cookie")._value
                    self.headers["Cookie"] = "blog_cookie=" + self.token
                else:
                    print(f'Login failed for user {self.username}')

    async def create_posts(self):
        url = "http://127.0.0.1:8000/post/"
        test = ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
        payload = {"user_id": 0, "text": str(test[0])}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                if response.status != 200:
                    print(f'The post has not been created')

    async def like_posts(self, post_id):
        url = "http://127.0.0.1:8000/post/like_post/" + str(post_id)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers) as response:
                if response.status != 200:
                    print(f'The post has not been liked')


async def register_users(users_set):
    for i in range(NUMBER_OF_USERS):
        username = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        password = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
        users_set.add(User(username=username, email=username, password=password))
    tasks = [user.register() for user in users_set]
    await asyncio.gather(*tasks)


async def login_users(users_set):
    tasks = [user.login() for user in users_set]
    await asyncio.gather(*tasks)


async def create_posts(users_set):
    tasks = []
    for user in users_set:
        tasks.extend([user.create_posts() for i in range(0, MAX_POSTS_PER_USER)])
    await asyncio.gather(*tasks)


async def like_posts(users_set):
    tasks = []
    for user in users_set:
        last_post = await user.get_last_post()
        tasks.extend([user.like_posts(random.randint(1, last_post)) for i in range(0, MAX_LIKES_PER_USER)])
    await asyncio.gather(*tasks)


async def main():
    users_set = set()
    await register_users(users_set)
    await login_users(users_set)
    await create_posts(users_set)
    await like_posts(users_set)

if __name__ == '__main__':
    asyncio.run(main())

# TODO: create Bot class to create users
