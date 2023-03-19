from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import *


def missing_params(mandatory_fields: list, input: list):
    missing_params = list(set(mandatory_fields) - set(input))
    if len(missing_params) > 0:
        missing = ", ".join([f"`{str(elem)}`" for elem in missing_params])
        return True, missing
    return False, None


class FollowDataSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    
    def follow_user(self, request):
        user = request.user
        validated_data = request.data
        follow_id = validated_data["id"]

        user_to_follow = get_user_model().objects.get(id=follow_id)
        follow_entry, created = UserData.objects.get_or_create(follower=user, following=user_to_follow)
        if created:
            message = "User followed successfully"
        else:
            message = "You are already following this user"
        return message 


    def unfollow_user(self, request):
        user = request.user
        validated_data = request.data
        follow_id = validated_data["id"]

        user_to_unfollow = get_user_model().objects.get(id=follow_id)
        unfollow_entry = UserData.objects.filter(follower=user, following=user_to_unfollow).first()
        if unfollow_entry:
            unfollow_entry.delete()
            message = "User unfollowed successfully"
        else:
            message = "You are not following this user"
        return message


    def get_user_details(self, request):
        user = request.user

        username = user.username
        no_of_followers = UserData.objects.filter(following=user)
        no_of_following = UserData.objects.filter(follower=user)

        return {
            "username": username,
            "no_of_followers": len(no_of_followers),
            "no_of_following": len(no_of_following)
        }


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=1000, required=False)

    def create_post(self, request):
        user = request.user
        validated_data = request.data

        mandatory_fields = ["title", "description"]
        any_params_missing, params = missing_params(
            mandatory_fields, validated_data.keys()
        )
        if any_params_missing:
            return f"{params} keys is/are missing in request"

        title = validated_data["title"]
        description = validated_data["description"]

        new_post = Post.objects.create(title=title, description=description, user=user)
        return "Post created successfully"

    def delete_post(self, request):
        user = request.user
        validated_data = request.data

        post_id = validated_data["id"]
        post = Post.objects.filter(id=post_id, user=user).first()
        if post:
            post.delete()
            return "Post deleted successfully"
        else:
            return "Post does not exist"

    def like_post(self, request):
        user = request.user
        validated_data = request.data

        post_id = validated_data["id"]
        post = Post.objects.filter(id=post_id).first()
        if post:
            like_entry, created = PostLikes.objects.get_or_create(post=post, user=user)
            if created:
                like_entry.liked = True
                like_entry.save()
                return "Post liked"
        else:
            return "Post does not exist"

    def unlike_post(self, request):
        user = request.user
        validated_data = request.data

        post_id = validated_data["id"]
        post = Post.objects.filter(id=post_id).first()
        if post:
            like_entry = PostLikes.objects.filter(post=post, user=user).first()
            if like_entry:
                like_entry.liked = False
                like_entry.save()
                return "Post unliked"
        else:
            return "Post does not exist"

    def comment_post(self, request):
        user = request.user
        validated_data = request.data

        post_id = validated_data["id"]
        comment = validated_data["comment"]
        post = Post.objects.filter(id=post_id).first()
        if post:
            comment_entry = PostComments.objects.create(post=post, user=user, comment=comment)
            return comment_entry.id
        else:
            return "Post does not exist"

    def get_post_data(self, request):
        user = request.user
        validated_data = request.GET.copy()

        mandatory_fields = ["id"]
        any_params_missing, params = missing_params(
            mandatory_fields, validated_data.keys()
        )
        if any_params_missing:
            return f"{params} keys is/are missing in request"

        post_id = validated_data["id"]
        post = Post.objects.filter(id=post_id).first()
        if post:
            post_data = {
                "post_id": post.id,
                "likes": len(PostLikes.objects.filter(post=post, liked=True)),
                "comments": len(PostComments.objects.filter(post=post))
            }
            return post_data
        else:
            return "Post does not exist"

    def get_all_posts(self, request):
        user = request.user
        posts = Post.objects.filter(user=user).order_by("created_at")
        post_comments = PostComments.objects.filter(post__in=posts)
        comments = []
        for comment in post_comments:
            comments.append(comment.comment)
        posts_data = []
        for post in posts:
            post_data = {
                "post_id": post.id,
                "title": post.title,
                "description": post.description,
                "created_at": post.created_at,
                "likes": len(PostLikes.objects.filter(post=post, liked=True)),
                "comments": comments

            }
            posts_data.append(post_data)
        return posts_data