"""users 應用程式的資料模型。"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from users.utils import generate_unique_slug


class Profile(models.Model):

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
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=True,
    )
    is_public = models.BooleanField(
        default=True,
        help_text="是否公開個人資料",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.full_name or self.user.username)
            self.slug = generate_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username or self.full_name
