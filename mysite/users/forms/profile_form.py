import re
from django import forms
from django.core.files.uploadedfile import UploadedFile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

from ..utils import generate_unique_slug
from ..models import Profile


class ProfileForm(forms.models.ModelForm):
    email = forms.EmailField(
        disabled=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "email",
            "age",
            "education",
            "avatar",
            "slug",
            "is_public",
        ]
        labels = {
            "full_name": "姓名",
            "email": "電子郵件",
            "age": "年齡",
            "education": "教育程度",
            "avatar": "頭像",
            "slug": "個人資料網址",
            "is_public": "公開個人資料",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "請輸入全名"}),
            "age": forms.NumberInput(attrs={"placeholder": "請輸入年齡"}),
            "education": forms.Select(),
            "avatar": forms.FileInput(
                attrs={
                    "accept": "image/png,image/jpeg,image/jpg",
                }
            ),
            "slug": forms.TextInput(attrs={"placeholder": "請輸入網址主體"}),
            "is_public": forms.CheckboxInput(),
        }
        error_messages = {
            "full_name": {
                "required": "請輸入姓名",
                "max_length": "姓名超過長度限制",
            },
            "age": {
                "required": "請輸入年齡",
                "invalid": "請輸入有效的年齡",
                "min_value": "年齡不能為負數",
            },
            "education": {"required": "請選擇教育程度"},
            "avatar": {"invalid_image": "請上傳有效的圖片"},
            "slug": {
                "required": "請輸入個人簡介網址",
                "invalid": "個人簡介網址只能包含字母、數字、下劃線和連字符",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("full_name"),
            Field("email"),
            Field("age"),
            Field("education"),
            Field("avatar"),
            Field("slug"),
            HTML(
                """
                <small class="form-text text-muted">
                    這會成為你公開網址的一部分
                </small>
            """
            ),
            Field("is_public"),
        )

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if not re.search(r"^[\u4e00-\u9fa5a-zA-Z0-9\s]+$", full_name):
            raise forms.ValidationError("姓名只能包含中文、英文和數字")
        return full_name

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and isinstance(avatar, UploadedFile):
            valid_extensions = ["png", "jpg", "jpeg"]
            if not avatar.name.lower().endswith(tuple(valid_extensions)):
                raise forms.ValidationError("請上傳有效的圖片格式（PNG或JPEG）")
            max_size = 2 * 1024 * 1024
            if avatar.size > max_size:
                raise forms.ValidationError("圖片大小不能超過2MB")

            if avatar.content_type not in ["image/png", "image/jpeg"]:
                raise forms.ValidationError("請上傳有效的圖片格式（PNG或JPEG）")

        return avatar

    def clean_slug(self):
        base_slug = self.cleaned_data.get("slug")
        if re.search(r"^[a-zA-Z0-9-]+$", base_slug) and "-" in base_slug:
            slug = base_slug
        else:
            slug = generate_unique_slug(base_slug, instance_pk=self.instance.pk)

        return slug

    def save(self, commit=True):
        profile = super().save(commit=False)

        fields = [
            "full_name",
            "age",
            "education",
            "avatar",
            "slug",
            "is_public",
        ]
        for field in fields:
            input_value = self.cleaned_data.get(field)
            if input_value in [None, "", "None"]:
                setattr(profile, field, getattr(self.instance, field))

        if commit:
            profile.save()
        return profile
