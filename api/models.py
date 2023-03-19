from django.db import models
from django.conf import settings

# Create your models here.
User = settings.AUTH_USER_MODEL

class UserData(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return self.user.username

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)


class PostComments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
