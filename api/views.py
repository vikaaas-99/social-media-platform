from django.shortcuts import render
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import *


# Create your views here.

@api_view(["POST"])
def follow_user(request):
    """
    Follow a user
    """
    serializer = FollowDataSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.follow_user(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def unfollow_user(request):
    """
    Unfollow a user
    """
    serializer = FollowDataSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.unfollow_user(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user_data(request):
    """
    Get user data
    """
    serializer = FollowDataSerializer(data=request)
    response = serializer.get_user_details(request)
    return Response(response, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_delete_post(request):
    """
    Create or delete a post based on input
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        data = request.data
        if "id" in data.keys():
            response = serializer.delete_post(request)
        else:
            response = serializer.create_post(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def like_post(request):
    """
    Like a post
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.like_post(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def unlike_post(request):
    """
    Unlike a post
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.unlike_post(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def comment_post(request):
    """
    Comment on a post
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.comment_post(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_post(request):
    """
    Get a post data
    """
    serializer = PostSerializer(data=request.GET)
    if serializer.is_valid():
        response = serializer.get_post_data(request)
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_posts(request):
    """
    Get all posts
    """
    serializer = PostSerializer(data=request)
    response = serializer.get_all_posts(request)
    return Response(response, status=status.HTTP_200_OK)

