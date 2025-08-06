"""users 應用程式的資料模型。"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """用戶資料模型，擴展 Django 的 User 模型。"""

    EDUCATION_CHOICES = [
        ("None", "無"),
        ("ES", "小學"),
        ("MS", "初中"),
        ("HS", "高中"),
        ("BA", "大學"),
        ("MA", "碩士"),
        ("PhD", "博士"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(
        max_length=100,
        null=True,
        default=None,
    )
    age = models.PositiveIntegerField(null=True, default=None)
    education = models.CharField(
        max_length=10,
        choices=EDUCATION_CHOICES,
        null=True,
        default=None,
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default.png",
    )

    def __str__(self):
        return self.user.username or self.full_name
