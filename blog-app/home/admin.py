from django.contrib import admin
from .models import BlogPost, Comment, Profile

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Profile)