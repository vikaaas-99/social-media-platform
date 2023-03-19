import names
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import *

# Create your tests here.

def generate_user(is_superuser: bool = False) -> User:
    User = get_user_model()
    user = User.objects.create_user(
        username=names.get_full_name(),
        email=f"{names.get_full_name()}@dev.com",
        password=names.get_full_name(),
        is_superuser=is_superuser,
    )
    return user

def generate_follow_user(user, user_to_follow):
    follow_entry, created = UserData.objects.get_or_create(follower=user, following=user_to_follow)
    if created:
        message = "User followed successfully"
    else:
        message = "You are already following this user"
    return message

def generate_post(user):
    post = Post.objects.create(user=user, title="test", description="this is a test post")
    return post

def generate_post_like(user, post):
    like = PostLikes.objects.create(user=user, post=post)
    return like

def generate_post_comment(user, post):
    comment = PostComments.objects.create(user=user, post=post, comment="this is a test comment")
    return comment


class FollowTests(APITestCase):
    def test_follow_user(self):
        """
        Ensure urls are auth protected
        """
        url = reverse("api:follow-user")
        data = {"id": 1}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserData.objects.filter().count(), 0)

        """
        follow a user
        """
        user = generate_user()
        user_to_follow = generate_user()
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:follow-user")

        data = {"id": user_to_follow.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserData.objects.filter().count(), 1)

        """
        follow a user again
        """
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "You are already following this user")

        """
        serializer error
        """
        data = {"id": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_unfollow_user(self):
        """
        unfollow a user
        """
        user = generate_user()
        user_to_follow = generate_user()

        generate_follow_user(user, user_to_follow)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:unfollow-user")

        data = {"id": user_to_follow.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "User unfollowed successfully")
        self.assertEqual(UserData.objects.filter().count(), 0)


        """
        not following a user
        """
        response = self.client.post(url, data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "You are not following this user")

        """
        serializer error
        """
        data = {"id": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_user_data(self):
        """
        get user data
        """
        user = generate_user()
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:get-user-data")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["no_of_followers"], 0)
        self.assertEqual(response.data["no_of_following"], 0)
        self.assertEqual(UserData.objects.filter().count(), 0)

        """
        in case of data
        """
        user = generate_user()
        user_to_follow = generate_user()
        generate_follow_user(user, user_to_follow)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        url = reverse("api:get-user-data")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], user.username)
        self.assertEqual(response.data["no_of_followers"], 0)
        self.assertEqual(response.data["no_of_following"], 1)


class PostTests(APITestCase):
    def test_create_delete_post(self):

        """
        create a post
        """
        user = generate_user()
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:create-delete-post")

        data = {"title": "This is a test post", "description": "This is a test post"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post created successfully")
        self.assertEqual(Post.objects.filter().count(), 1)

        """
        in case of invalid data
        """
        data = {"title": "This is a test post"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "`description` keys is/are missing in request")

        """
        delete a post
        """
        user = generate_user()
        post = generate_post(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:create-delete-post")

        data = {"id": post.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post deleted successfully")
        self.assertEqual(Post.objects.filter().count(), 1)

        """
        serializer error
        """
        data = {"id": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """
        post does not exist
        """
        data = {"id": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post does not exist")


    def test_get_user_posts(self):
        """
        get user posts
        """
        user = generate_user()
        post = generate_post(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:get-post-data")

        response = self.client.get(url + f"?id={post.id}", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["likes"], 0)
        self.assertEqual(Post.objects.filter().count(), 1)

        """
        in case of missing `id`
        """
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "`id` keys is/are missing in request")

        """
        in case of post does not exist
        """
        response = self.client.get(url + f"?id=100", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post does not exist")

        """
        serialiser error
        """
        response = self.client.get(url + f"?id=abc", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 


    def test_like_post(self):
        """
        like a post
        """
        user = generate_user()
        post = generate_post(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:like-post")

        data = {"id": post.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post liked")
        self.assertEqual(PostLikes.objects.get(post=post).liked, True)

        """
        serialiser error
        """
        data = {"id": "abc"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 


        """
        post does not exist
        """
        data = {"id": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post does not exist")


    def test_unlike_post(self):
        """
        unlike a post
        """
        user = generate_user()
        post = generate_post(user)
        like = generate_post_like(user, post)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:unlike-post")

        data = {"id": post.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data, "Post unliked")
        self.assertEqual(PostLikes.objects.get(post=post).liked, False)

        """
        serialiser error
        """
        data = {"id": "abc"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """
        post does not exist
        """
        data = {"id": 100}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post does not exist")


    def test_post_comments(self):
        """
        post a comment
        """
        user = generate_user()
        post = generate_post(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:comment-post")

        data = {"id": post.id, "comment": "This is a test comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PostComments.objects.get(post=post).id)
        self.assertEqual(PostComments.objects.filter().count(), 1)

        """
        serialiser error
        """
        data = {"id": "abc", "comment": "This is a test comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        """
        post does not exist
        """
        data = {"id": 100, "comment": "This is a test comment"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Post does not exist")

    
    def test_get_all_posts(self):
        """
        get all posts
        """
        user = generate_user()
        post = generate_post(user)
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        url = reverse("api:get-all-posts")

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["post_id"], post.id)

        """
        when post has comments also
        """
        comment = generate_post_comment(user, post)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["post_id"], post.id)
        self.assertEqual(len(response.data[0]["comments"]), 1)