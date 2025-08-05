"""polls 應用程式的後台管理設定。"""
from django.contrib import admin
from .models import Question

admin.site.register(Question)
