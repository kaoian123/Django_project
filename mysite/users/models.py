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

    def update_profile(
            self,
            full_name=None,
            age=None,
            education=None,
            avatar=None):
        """更新用戶資料的方法。"""
        if full_name is not None:
            self.full_name = full_name
        if age is not None:
            self.age = age
        if education is not None:
            self.education = education
        if avatar is not None:
            self.avatar = avatar
        self.save()

    def __str__(self):
        return self.user.username or self.full_name
