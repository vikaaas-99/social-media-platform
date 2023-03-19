from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


@admin.register(PostComments)
class PostCommentsAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
