from django.urls import include, path

from .models import *
from .views import *

app_name = "api"
urlpatterns = [
    path("follow/", follow_user, name="follow-user"),
    path("unfollow/", unfollow_user, name="unfollow-user"),
    path("user/", get_user_data, name="get-user-data"),
    path("posts/", create_delete_post, name="create-delete-post"),
    path("like/", like_post, name="like-post"),
    path("unlike/", unlike_post, name="unlike-post"),
    path("comment/", comment_post, name="comment-post"),
    path("post/", get_post, name="get-post-data"),
    path("all_posts/", get_all_posts, name="get-all-posts"),
]
