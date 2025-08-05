"""users app 的後台管理設定。"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
